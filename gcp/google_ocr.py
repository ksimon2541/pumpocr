# This script was used as a prototype to validate if google cloud vision API was a good fit for what I was trying to accomplish.

judgements = ['PERFECT', 'GREAT', 'GOOD', 'BAD', 'MISS']
def detect_text(path: object) -> object:
    """Detects text in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image) 

    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

def get_text_data(path):
    """Detects text in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    return texts

def is_left(midpoint, vertices):
    return midpoint[0] >= vertices[1].x

def same_row(midpoint, vertices):
    return midpoint[1] >= vertices[0].y and midpoint[1] <= vertices[2].y

def isnumericlike(numeric):
    for digit in numeric:
        if not digit.isnumeric() and not digit == 'O':
            return False
    return True


def find_judgement_count(texts, judgement):
    current = None
    midpoint = get_midpoint(judgement.bounding_poly.vertices)
    for text in texts:
        text_vertices = text.bounding_poly.vertices
        if isnumericlike(text.description) and is_left(midpoint, text_vertices) and same_row(midpoint, text_vertices):
            current = text
    if current == None:
        return 'Not found'
    else:
        return current.description

def get_midpoint(vertices):
    mid_x = (vertices[0].x + vertices[1].x) / 2
    mid_y = (vertices[0].y + vertices[2].y) / 2
    return (mid_x, mid_y)


def process_texts(texts):
    text_pairs = []
    for text in texts:
        if text.description in judgements:
            jc_description = find_judgement_count(texts, text)
            text_pairs.append((text.description, jc_description))
        # todo: Handle non judgement text
    return text_pairs


img_path = "/home/simo/Development/pumpocr/img/cleaner_rotated_test.jpg"
detect_text(img_path)
#text_data = get_text_data(img_path)
#pairs = process_texts(text_data)
#for pair in pairs:
#    print("{}\n".format(pair))
