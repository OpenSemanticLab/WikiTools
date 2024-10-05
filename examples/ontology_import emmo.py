import os

from osw.auth import CredentialManager
from osw.core import model
from osw.express import OswExpress
from osw.ontology import ImportConfig, OntologyImporter, ParserSettings

# Use credentials from file. if none are found, the user will be prompted to enter them
cm = CredentialManager(
    cred_filepath=os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "accounts.pwd.yaml"
    )
)
# Create the OSW object
osw_obj = OswExpress(domain="wiki-dev.open-semantic-lab.org", cred_mngr=cm)
# Load the required schemas / data classes
DEPENDENCIES = {
    "OwlClass": "Category:OSW725a3cf5458f4daea86615fcbd0029f8",
    "OwlIndividual": "Category:OSW6b9ef2784a934b8ab96523366e23e906",
    "EmmoClass": "Category:OSW57beed5e1294434ba77bb6516e461456",
    "Item": "Category:Item",
    "ObjectProperty": "Category:ObjectProperty",
    "DataProperty": "Category:DataProperty",
    "AnnotationProperty": "Category:AnnotationProperty",
}
osw_obj.install_dependencies(DEPENDENCIES, mode="append")

ontology_name = "BVCO"

# Define ontology metadata
emmo = model.Ontology(
    name="EMMO",
    iri="http://emmo.info/emmo",
    prefix="http://emmo.info/emmo#",
    prefix_name="emmo",
    link="https://github.com/emmo-repo/EMMO",
)
dc = model.Ontology(
    name="DC",
    iri="http://purl.org/dc/elements/1.1",
    prefix="http://purl.org/dc/elements/1.1/",
    prefix_name="dc",
    link="http://purl.org/dc",
)
battinfo = model.Ontology(
    name="EMMO BattINFO",
    iri="http://emmo.info/battery",
    prefix="http://emmo.info/battery#",
    prefix_name="battinfo",
    link="https://github.com/BIG-MAP/BattINFO",
)
electrochemistry = model.Ontology(
    name="EMMO Electrochemistry",
    iri="http://emmo.info/electrochemistry",
    prefix="http://emmo.info/electrochemistry#",
    prefix_name="electrochemistry",
    link="https://github.com/emmo-repo/EMMO",
)
periodictable = model.Ontology(
    name="EMMO Periodic Table",
    iri="http://emmo.info/emmo/domain/periodic-table",
    prefix="http://emmo.info/emmo/domain/periodic-table#",
    prefix_name="periodictable",
    link="https://github.com/emmo-repo/EMMO",
)
gpo = model.Ontology(
    name="GPO",
    iri="https://gpo.ontology.link",
    prefix="https://gpo.ontology.link/",
    prefix_name="gpo",
    link="https://github.com/General-Process-Ontology/ontology",
)
bvco = model.Ontology(
    name="BVCO",
    iri="https://bvco.ontology.link",
    prefix="https://bvco.ontology.link/",
    prefix_name="bvco",
    link="https://github.com/Battery-Value-Chain-Ontology/ontology",
)

import_config = ImportConfig(
    ontology_name=ontology_name,
    ontologies=[emmo, dc, battinfo, electrochemistry, periodictable, gpo, bvco],
    # file="https://raw.githubusercontent.com/BIG-MAP/BattINFO/master/battinfo.ttl",
    file="https://raw.githubusercontent.com/emmo-repo/domain-battery/master/battery.ttl",
    base_class=model.EmmoClass,
    base_class_title="Category:OSW57beed5e1294434ba77bb6516e461456",  # EmmoClass
    dump_files=True,
    dump_path=os.path.dirname(os.path.abspath(__file__)),
    dry_run=False,
)
parser_settings = ParserSettings()
parser_settings.ensure_array.append("elucidation")
parser_settings.ensure_multilang.append("elucidation")

# Import ontologies
importer = OntologyImporter(osw=osw_obj, parser_settings=parser_settings)
importer.import_ontology(import_config)
