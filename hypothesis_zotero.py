import json
import h_annot
from pyzotero import zotero, zotero_errors

from settings import library_id, zot_api_key, hyp_username, hyp_api_key, num2grab

def format_converted_note(annotation):
    """Format an annotation so that it translates properly into Zotero note markup."""
    annotated_text = extract_exact(annotation)
    annotation_text = annotation["text"]
    return """<p style="color: green; text-align: center;">{}</p>
    <br>
    <p>{}</p>""".format(annotated_text, annotation_text)

def extract_exact(annotation):
    try:
        annotation["target"][0]["selector"]
    except KeyError as e:
        print(annotation)
        return "<text not available>"
    for selector in annotation["target"][0]["selector"]:
        try:
            return selector["exact"]
        except KeyError:
            continue
    return None

def extract_note_tags(notes):
    tags = set()
    for note in notes:
        for tag in note['data']['tags']:
            tags.add(tag['tag'])
    return tags

def grab():
    zot = zotero.Zotero(library_id, 'user', zot_api_key)

    items = zot.top(limit=num2grab)

    for entry_i in enumerate(items):
        entry = entry_i[1]
        try:
            entry_children = zot.children(entry['key'])
        except zotero_errors.UnsupportedParams as e:
            print(dir(e))
            print(f"Skipping due to error: {e}")
            continue
        notes = [note for note in entry_children if note['data']['itemType'] == 'note']
        tags = extract_note_tags(notes)
        url = entry['data']['url']
        if len(url) == 0:
            continue
        print(f"Checking {url}")
        entry_annotations = json.loads(h_annot.api.search(hyp_api_key,
                                                          url=entry['data']['url'],
                                                          user=hyp_username))["rows"]
        if len(entry_annotations) == 0:
            continue

        note_imports = []
        template = zot.item_template("note")

        def get_annotation_start(annotation):
            selectors = annotation['target'][0]['selector']
            text_position_sel = list(filter(lambda sel: sel['type'] == 'TextPositionSelector', selectors))
            return text_position_sel[0]['start']

        entry_annotations.sort(key=lambda annotation: get_annotation_start(annotation))
        for annotation in entry_annotations:
            if annotation["id"] in tags:
                continue
            else:
                print("Found new item")
                template['tags'] = (annotation['tags'].copy() +
                                    [{"tag": annotation["id"], "type":1}] +
                                    [{"tag": "hyp-annotation", "type":1}])
                template['note'] += format_converted_note(annotation)
        note_imports.append(template)
        #TODO: Fix this so it doesn't break if you have more than 50 annotations on a document
        zot.create_items(note_imports, entry["key"])

grab()
