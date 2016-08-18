# Coral_json2sql
Create a convert from JSON format to SQL format to import data in Coral


## Logical
- "type" field from json file will not be preserved.
- "access_type" field from json file will correspond to "Access" tab, "Authentication Type" field.
- "ID" field from json file will correspond to "Product" tab, "Record ID" field.
- "DESCRIPTION" field from json file will correspond to "Product" tab, "English description" field.
- "LABEL" field from json file will not be preserved.
- "TITLE" field from json file will correspond to header.
- "Lang" field from json file will correspond to "Product" tab, "Language" field.
- "URL\_REMOTE\_RES", "URL\_LOCAL\_RES" and "URL\_FREE\_RES" fields from json file will correspond to header "Product" tab, "Resource URL" field. The first mentionned field will have the priority.
- "RELEVANCE" field from json file will not be preserved.
- "CLASSEMENT_TYPE" field from json file will correspond to "Product" tab, "Type" field.
- "ANALYTICS_ID" field from json file will not be preserved.
- "short_description" field from json file will not be preserved.
- "access_right" field from json file will not be preserved.
- "label" field from json file will not be preserved.
- "title" field from json file will not be preserved.
- "az" field from json file will not be preserved.
- "lang" field from json file will not be preserved.
- "category" field from json file will correspond to "Product" tab, "Subjects" array.


## Credits

[Sciences Po - Library](http://www.sciencespo.fr/bibliotheque/en)


## Licenses
[LGPL V3.0](http://www.gnu.org/licenses/lgpl.txt "LGPL V3.0")

[CECILL-C](http://www.cecill.info/licences/Licence_CeCILL-C_V1-fr.html "CECILL-C")