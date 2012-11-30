#import pdfminer
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage

#method


def parse_lt_objs (lt_objs, page_number, images_folder, text=[]):
    """Iterate through the list of LT* objects and capture the text or image data contained in each"""
    text_content = [] 

    for lt_obj in lt_objs:
        if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
            # text
            text_content.append(lt_obj.get_text())
        #elif isinstance(lt_obj, LTImage):
            # an image, so save it to the designated folder, and note it's place in the text 
        #    saved_file = save_image(lt_obj, page_number, images_folder)
        #    if saved_file:
                # use html style <img /> tag to mark the position of the image within the text
        #        text_content.append('<img src="'+os.path.join(images_folder, saved_file)+'" />')
        #    else:
        #        print >> sys.stderr, "Error saving image on page", page_number, lt_obj.__repr__
        elif isinstance(lt_obj, LTFigure):
            # LTFigure objects are containers for other LT* objects, so recurse through the children
            text_content.append(parse_lt_objs(lt_obj, page_number, images_folder, text_content))
            #print 1

    return '\n'.join(text_content)

# Open a PDF file.
fp = open('insurance1.pdf', 'rb')
# Create a PDF parser object associated with the file object.
parser = PDFParser(fp)
# Create a PDF document object that stores the document structure.
doc = PDFDocument()
# Connect the parser and document objects.
parser.set_document(doc)
doc.set_parser(parser)
# Supply the password for initialization.
# (If no password is set, give an empty string.)
doc.initialize('')
# Check if the document allows text extraction. If not, abort.
if not doc.is_extractable:
    raise PDFTextExtractionNotAllowed
rsrcmgr = PDFResourceManager()
#container
text_content = []

laparams = LAParams()
# Create a PDF page aggregator object.
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)
i=0
for page in doc.get_pages():
    interpreter.process_page(page)
    # receive the LTPage object for the page.
    layout = device.get_result()
    text_content.append(parse_lt_objs(layout, (i+1), '/converter'))
    i=i+1
print text_content
'''# Create a PDF resource manager object that stores shared resources.
rsrcmgr = PDFResourceManager()
# Create a PDF device object.
device = PDFDevice(rsrcmgr)
# Create a PDF interpreter object.
interpreter = PDFPageInterpreter(rsrcmgr, device)
# Process each page contained in the document.
for page in doc.get_pages():
    interpreter.process_page(page)
    print page'''
