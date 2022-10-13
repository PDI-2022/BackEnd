import email
import cv2
import numpy as np
import base64
import csv
from api.grid_cut import cortar_malha as cut

def extract_white_percentage(input_image):
    hsv = cv2.cvtColor(input_image, cv2.COLOR_BGR2HSV)

    lower = np.array([0,0,168])
    upper = np.array([172,111,255])   
    mask = cv2.inRange(hsv, lower, upper)

    white_extracted_image = cv2.bitwise_and(input_image, input_image, mask = mask)

    pixels_number_seed = np.count_nonzero(input_image)
    pixels_extracted_white = np.count_nonzero(white_extracted_image)

    return pixels_extracted_white/pixels_number_seed


def remove_background(input_image):
    used_threshold, thresholded_bgr_image = cv2.threshold(input_image, 110, 255, cv2.THRESH_BINARY)
    thresholded_blue_component, thresholded_green_component, thresholded_red_component = cv2.split(thresholded_bgr_image)

    mask_filtered = cv2.medianBlur(thresholded_red_component, 5)

    result_image = cv2.bitwise_and(input_image, input_image, mask = mask_filtered)

    return result_image


def extract_dark_red_percentage(input_image, id=0):
    hsv = cv2.cvtColor(input_image, cv2.COLOR_BGR2HSV)

    lower = np.array([161, 168, 80])
    upper = np.array([180 , 255, 240])   
    mask = cv2.inRange(hsv, lower, upper)

    white_extracted_image = cv2.bitwise_and(input_image, input_image, mask = mask)

    pixels_number_seed = np.count_nonzero(input_image)
    pixels_extracted_white = np.count_nonzero(white_extracted_image)

    return pixels_extracted_white/pixels_number_seed


def extract_light_red_percentage(input_image, id=0):
    hsv = cv2.cvtColor(input_image, cv2.COLOR_BGR2HSV)

    lower = np.array([161,90,80])
    upper = np.array([180,190,240])   
    mask = cv2.inRange(hsv, lower, upper)

    white_extracted_image = cv2.bitwise_and(input_image, input_image, mask = mask)

    pixels_number_seed = np.count_nonzero(input_image)
    pixels_extracted_white = np.count_nonzero(white_extracted_image)

    return pixels_extracted_white/pixels_number_seed

def remove_empty_blocks(intern, extern):
    pass

def process_data(intern, extern):
    buffer_intern = base64.b64decode(intern)
    nparr = np.frombuffer(buffer_intern, np.uint8)
    input_intern_image = cv2.imdecode(nparr, flags=1)

    buffer_extern = base64.b64decode(extern)
    nparr = np.frombuffer(buffer_extern, np.uint8)
    input_extern_image = cv2.imdecode(nparr, flags=1)

    intern_seeds = cut(input_intern_image)
    extern_seeds = cut(input_extern_image)

    header = ['Semente', 'Lado', 'Porcentagem de Branco', 'Porcentagem de Vermelho Carmim Claro', 'Porcentagem de Vermelho Carmim Escuro']
    rows = []

    for i, seed in enumerate(intern_seeds):
        if not is_empty(seed):
            removed_background = remove_background(seed)
            white_percentage = extract_white_percentage(removed_background)
            light_red_percentage = extract_light_red_percentage(removed_background)
            dark_red_percentage = extract_dark_red_percentage(removed_background)

            rows.append(
                [
                    i + 1, 
                    'Interno', 
                    f'{white_percentage*100:.2f}%', 
                    f'{light_red_percentage*100:.2f}%',
                    f'{dark_red_percentage*100:.2f}%'
                ]
            )
    
    for i, seed in enumerate(extern_seeds):
        if not is_empty(seed):
            removed_background = remove_background(seed)
            white_percentage = extract_white_percentage(removed_background)
            light_red_percentage = extract_light_red_percentage(removed_background)
            dark_red_percentage = extract_dark_red_percentage(removed_background)

            rows.append(
                [
                    i + 1, 
                    'Externo', 
                    f'{white_percentage*100:.2f}%', 
                    f'{light_red_percentage*100:.2f}%',
                    f'{dark_red_percentage*100:.2f}%'
                ]
            )

    with open('relatorio.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)
        
    return 'relatorio.csv'

def is_empty(block):
    removed_background = remove_background(block)
    percentage = np.count_nonzero(remove_background) / (block.shape[0]*block.shape[1])

    return False if percentage < 0.05 else True
