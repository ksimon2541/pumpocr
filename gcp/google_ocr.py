def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
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

def starts_with_alpha(text):
    return text[0].isalpha

def compare_coordinates(alpha_coordinates, numeric_coordinates):
    total = 0
    for alpha_c in alpha_coordinates:
        for numeric_c in numeric_coordinates:
            total += abs(alpha_c.y - numeric_c.y)
    return total

def process_texts(texts):
    text_pairs = []
    for alpha_text in texts:
        closest = (None, 10000000000)
        if alpha_text.description.isalpha():
            for numeric_text in texts:
                if numeric_text.description.isnumeric():
                    difference = compare_coordinates(alpha_text.bounding_poly.vertices, numeric_text.bounding_poly.vertices)
                    if difference < closest[1]:
                        closest = (numeric_text, difference)
            text_pairs.append((alpha_text.description, closest[0].description))
    return text_pairs

img_path = "/home/simo/Development/pumpocr/img/baroque_test.png"
text_data = get_text_data(img_path)
pairs = process_texts(text_data)
for pair in pairs:
    print("{}\n".format(pair))
