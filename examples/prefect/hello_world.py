import asyncio
import uuid
from os import environ
from typing import Optional
from uuid import UUID, uuid4

from prefect import flow, get_client, task
from prefect.blocks.system import Secret
from pydantic import Field

import osw.model.entity as model
from osw.auth import CredentialManager
from osw.core import OSW
from osw.utils.wiki import get_full_title
from osw.wtsite import WtSite


class ConnectionSettings(model.OswBaseModel):
    """Connection data for OSW"""

    osw_user_name: Optional[str]
    """The login username.
    Note: value of envar OSW_USER used of not given
    Note: value of envar OSW_PASSWORD used for login"""
    osw_domain: Optional[str]
    """The domain of the instance
    Note: value of envar OSW_SERVER used of not given"""


@task
def connect(settings: Optional[ConnectionSettings] = ConnectionSettings()):
    """Initiates the connection to the OSW instance

    Parameters
    ----------
    settings
        see ConnectionSetttings dataclass
    """
    global wtsite
    # define username
    if environ.get("OSW_USER") is not None and environ.get("OSW_USER") != "":
        settings.osw_user_name = environ.get("OSW_USER")
    if environ.get("OSW_SERVER") is not None and environ.get("OSW_SERVER") != "":
        settings.osw_domain = environ.get("OSW_SERVER")
    password = ""
    if environ.get("OSW_PASSWORD") is not None and environ.get("OSW_PASSWORD") != "":
        password = environ.get("OSW_PASSWORD")
    else:
        # fetch secret stored in prefect server from calculated name
        password = Secret.load(
            settings.osw_user_name.lower() + "-" + settings.osw_domain.replace(".", "-")
        ).get()  # e. g. mybot-wiki-dev-open-semantic-lab-org
    cm = CredentialManager()
    cm.add_credential(
        CredentialManager.UserPwdCredential(
            iri=settings.osw_domain, username=settings.osw_user_name, password=password
        )
    )
    wtsite = WtSite(WtSite.WtSiteConfig(iri=settings.osw_domain, cred_mngr=cm))
    global osw
    osw = OSW(site=wtsite)


@task
def fetch_schema():
    """this will load the current entity schema from the OSW instance."""
    # Load Article Schema on demand
    if not hasattr(model, "Article"):
        osw.fetch_schema(
            OSW.FetchSchemaParam(
                schema_title=[
                    "Category:OSW77e749fc598341ac8b6d2fff21574058",  # Software
                    "Category:OSW72eae3c8f41f4a22a94dbc01974ed404",  # PrefectFlow
                    "Category:OSW92cc6b1a2e6b4bb7bad470dfdcfdaf26",  # Article
                ],
                mode="replace",
            )
        )


class Result(model.OswBaseModel):
    """The result dataclass"""

    uuid: Optional[UUID] = Field(default_factory=uuid4, title="UUID")
    """UUIDv4 of the result (autogenerated)"""
    target_title: Optional[str] = None
    """the target title to store the result.
    Autogenerated from uuid if not given
    """
    msg: str
    """The message you want to leave on the target page"""


@task
def store_and_document_result(result: Result):
    """Store workflow results on an OSW entry

    Parameters
    ----------
    result
        see Result dataclass
    """
    if result.target_title:
        title = result.target_title
    else:
        title = "Item:" + osw.get_osw_id(result.uuid)
    entity = osw.load_entity(title)
    if entity is None:
        # does not exist yet - create a new one
        entity = model.Article(
            uuid=result.uuid, label=[model.Label(text="Article for dummy workflow")]
        )

    # edit structured data
    entity = entity.cast(model.Article)
    entity.description = [model.Description(text="some descriptive text")]
    osw.store_entity(entity)

    # edit unstructured data (ToDo: access page directly from entity)
    page = osw.site.get_page(WtSite.GetPageParam(titles=[title])).pages[0]
    page.set_slot_content(
        slot_key="main", content=page.get_slot_content("main") + "<br>\n" + result.msg
    )
    page.edit()
    print("FINISHED")


class Request(model.OswBaseModel):
    uuid: UUID = Field(default_factory=uuid4, title="UUID")
    """UUIDv4 of the request."""
    osw_domain: Optional[str] = "wiki-dev.open-semantic-lab.org"
    """To domain of the OSW instance"""
    subject: Optional[str] = "Item:OSW56f9439d43244fe7a83163bab9414ee1"
    """Where to store the results. For testing, we use a static default value"""
    msg: Optional[str] = "test message"
    """The message you want to leave on the target page"""


@flow(
    name="Dummy Workflow",
    description="Dummy workflow that prints a message on a target page",
)
def dummy_workflow(request: Request):
    """Dummy workflow that prints a message on a target page

    Parameters
    ----------
    request
        see Request dataclass
    """
    connect(ConnectionSettings(osw_domain=request.osw_domain))
    fetch_schema()
    store_and_document_result(Result(msg=request.msg, target_title=request.subject))


async def deploy():
    """programmatic deployment supported in newer prefect versions"""
    flow = dummy_workflow
    # flow_name = flow.name
    deployment_name = flow.name + " Deployment"

    # create a deployment and apply it
    config = await flow.to_deployment(name=deployment_name)
    await config.apply()  # returns the deployment_uuid

    # fetch flow uuid
    async with get_client() as client:
        response = await client.read_flow_by_name(flow.name)
        print(response.json())
        flow_uuid = response.id

    await connect()
    await fetch_schema()
    # static UUIDv5 namespace for a stable UUID
    namespace_uuid = uuid.UUID("0dd6c54a-b162-4552-bab9-9942ccaf4f41")

    # self-documentation / registration
    this_tool = model.Software(
        uuid=uuid.uuid5(namespace_uuid, flow.name),
        label=[model.Label(text=flow.name)],
        description=[model.Description(text=flow.description)],
    )

    prefect_domain = environ.get("PREFECT_API_URL").split("//")[-1].split("/")[0]
    this_flow = model.PrefectFlow(
        uuid=flow_uuid,
        label=[model.Label(text=flow.name + " Prefect Flow")],
        description=[model.Description(text=flow.description)],
        flow_id=str(flow_uuid),
        hosted_software=[get_full_title(this_tool)],
        domain=prefect_domain,
    )

    osw.store_entity(osw.StoreEntityParam(entities=[this_tool, this_flow]))

    # start agent to serve deployment
    await dummy_workflow.serve(name=deployment_name)


if __name__ == "__main__":
    # dummy_workflow(Request(msg="Test"))
    with asyncio.Runner() as runner:
        runner.run(deploy())
