from io import BytesIO
import cv2
from itsdangerous import base64_encode
import numpy as np
import base64
import csv
from api.grid_cut import cortar_malha as cut
from skimage import measure
from shapely.geometry import Polygon

import api.classificacao as classificacao

def count_holes(image) -> int:
    contours = measure.find_contours(image, 200)

    holes = [Polygon(contour) for contour in contours if len(contour) > 3]
    
    seed_polygons = []
    
    #ordenando pela maior área (as duas maiores áreas são os próprio feijão)
    holes.sort(reverse=True, key=lambda element: element.area)

    within = [] 
    up = 0
    down = 0    
    

    # checando se tem buracos
    if len(holes) > 2:
        for i in range(2):
            seed_polygons.append(holes[i])
            down += holes[i].area
            

        holes.pop(0)
        holes.pop(0)

        for hole in holes:
            for seed_polygon in seed_polygons:
                if hole.within(seed_polygon):
                    within.append(hole)
                    up += hole.area

        return (len(within), (up/down))

    return (0, 0) 

def remove_background_and_get_mask(input_image):
    used_threshold, thresholded_bgr_image = cv2.threshold(input_image, 110, 255, cv2.THRESH_BINARY)
    thresholded_blue_component, thresholded_green_component, thresholded_red_component = cv2.split(thresholded_bgr_image)

    mask_filtered = cv2.medianBlur(thresholded_red_component, 5)

    return mask_filtered

def extract_white_percentage(input_image, id=0):
    hsv = cv2.cvtColor(input_image, cv2.COLOR_BGR2HSV)

    lower = np.array([0,0,168])
    upper = np.array([172,111,255])   
    mask = cv2.inRange(hsv, lower, upper)

    white_extracted_image = cv2.bitwise_and(input_image, input_image, mask = mask)

    pixels_number_seed = np.count_nonzero(input_image)
    pixels_extracted_white = np.count_nonzero(white_extracted_image)

    cv2.imwrite(f'./images/white_extract/white_{id}.jpg', np.hstack([input_image, white_extracted_image]))

    return pixels_extracted_white/pixels_number_seed


def remove_background(input_image, id=0):
    used_threshold, thresholded_bgr_image = cv2.threshold(input_image, 110, 255, cv2.THRESH_BINARY)
    thresholded_blue_component, thresholded_green_component, thresholded_red_component = cv2.split(thresholded_bgr_image)

    mask_filtered = cv2.medianBlur(thresholded_red_component, 5)

    result_image = cv2.bitwise_and(input_image, input_image, mask = mask_filtered)

    cv2.imwrite(f'./images/background_remove/remove_background_{id}.jpg', result_image)

    return result_image


def extract_dark_red_percentage(input_image, id=0):
    hsv = cv2.cvtColor(input_image, cv2.COLOR_BGR2HSV)

    first_lower = np.array([161, 168, 80])
    first_upper = np.array([180 , 255, 240])   
    first_mask = cv2.inRange(hsv, first_lower, first_upper)

    second_lower = np.array([0, 168, 80])
    second_upper = np.array([60 , 255, 240])   
    second_mask = cv2.inRange(hsv, second_lower, second_upper)

    mask = cv2.bitwise_or(first_mask, second_mask)

    dark_red_extracted_image = cv2.bitwise_and(input_image, input_image, mask = mask)

    pixels_number_seed = np.count_nonzero(input_image)
    pixels_extracted_white = np.count_nonzero(dark_red_extracted_image)

    cv2.imwrite(f'./images/red_extract/dark_red_mask{id}.jpg', np.hstack([input_image, dark_red_extracted_image]))

    return pixels_extracted_white/pixels_number_seed


def extract_light_red_percentage(input_image, id=0):
    hsv = cv2.cvtColor(input_image, cv2.COLOR_BGR2HSV)

    first_lower = np.array([161, 90, 80])
    first_upper = np.array([180 , 190, 240])   
    first_mask = cv2.inRange(hsv, first_lower, first_upper)

    second_lower = np.array([0, 90, 80])
    second_upper = np.array([60 , 190, 240])   
    second_mask = cv2.inRange(hsv, second_lower, second_upper)

    mask = cv2.bitwise_or(first_mask, second_mask)

    light_red_extracted_image = cv2.bitwise_and(input_image, input_image, mask = mask)

    pixels_number_seed = np.count_nonzero(input_image)
    pixels_extracted_white = np.count_nonzero(light_red_extracted_image)

    cv2.imwrite(f'./images/red_extract/light_red_mask_{id}.jpg', np.hstack([input_image, light_red_extracted_image]))

    return pixels_extracted_white/pixels_number_seed

def createCutImgsFold(index):
    externo = cv2.imread(f"./images/background_remove/remove_background_externo{index}.jpg")
    interno = cv2.imread(f"./images/background_remove/remove_background_interno{index}.jpg")

    cv2.imwrite(f'./images/imagens_cortadas/images/semente-' + str(index+1) + '.jpg', np.hstack([externo, interno]))

def process_data(intern, extern, genImg=False):
    buffer_intern = base64.b64decode(intern)
    nparr = np.frombuffer(buffer_intern, np.uint8)
    input_intern_image = cv2.imdecode(nparr, flags=1)

    buffer_extern = base64.b64decode(extern)
    nparr = np.frombuffer(buffer_extern, np.uint8)
    input_extern_image = cv2.imdecode(nparr, flags=1)
    intern_seeds = cut(input_intern_image)
    extern_seeds = cut(input_extern_image)

    header = ['Semente', 'Lado', 'Porcentagem de Branco', 'Porcentagem de Vermelho Carmim Claro', 'Porcentagem de Vermelho Carmim Escuro', 'Quantidade de Buracos', 'Área Buraco/Área Semente']
    rows = []

    for i, seed in enumerate(intern_seeds):
        if not is_empty(seed):
            removed_background = remove_background(seed, f'interno{i}')
            white_percentage = extract_white_percentage(removed_background, f'interno{i}')
            light_red_percentage = extract_light_red_percentage(removed_background, f'interno{i}')
            dark_red_percentage = extract_dark_red_percentage(removed_background, f'interno{i}')

            thresholded_red_component = remove_background_and_get_mask(seed)
            (holes, holes_percentage) = count_holes(thresholded_red_component)

            rows.append(
                [
                    i + 1, 
                    'Interno', 
                    f'{white_percentage*100:.2f}%', 
                    f'{light_red_percentage*100:.2f}%',
                    f'{dark_red_percentage*100:.2f}%',
                    holes,
                    f'{holes_percentage*100:.2f}%'
                ]
            )        
    for i, seed in enumerate(extern_seeds):
        if not is_empty(seed):
            removed_background = remove_background(seed, f'externo{i}')
            white_percentage = extract_white_percentage(removed_background, f'externo{i}')
            light_red_percentage = extract_light_red_percentage(removed_background, f'externo{i}')
            dark_red_percentage = extract_dark_red_percentage(removed_background, f'externo{i}')

            thresholded_red_component = remove_background_and_get_mask(seed)
            (holes, holes_percentage) = count_holes(thresholded_red_component)
            createCutImgsFold(i)

            rows.append(
                [
                    i + 1, 
                    'Externo', 
                    f'{white_percentage*100:.2f}%', 
                    f'{light_red_percentage*100:.2f}%',
                    f'{dark_red_percentage*100:.2f}%',
                    holes,
                    f'{holes_percentage*100:.2f}%'
                ]
            )

    with open('relatorio.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)

    classificacao.classificacao()

    if(genImg):
        return GenImg(intern_seeds,extern_seeds)
    return 'relatorio.csv'



def is_empty(block):
    removed_background = remove_background(block)
    percentage = np.count_nonzero(removed_background) / (block.shape[0]*block.shape[1])

    return True if percentage < 0.05 else False

def GenImg(intern_seeds,extern_seeds):
    intSeed = []
    extSeed = []
    for i,intt in enumerate(intern_seeds):
        if not is_empty(intt):
            intSeed.append({"id":i,"blob":str(base64.b64encode(cv2.imencode(".jpg",intt)[1]))})

    for i,extt in enumerate(extern_seeds):
        if not is_empty(extt):
            extSeed.append({"id":i,"blob":str(base64.b64encode(cv2.imencode(".jpg",extt)[1]))})

    csvJson = csv_to_json('relatorio.csv')

    return csvJson,intSeed,extSeed

def csv_to_json(csvFilePath):
    jsonArray = []
      
    #read csv file
    with open(csvFilePath, encoding='utf-8') as csvf: 
        #load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf) 

        #convert each csv row into python dict
        for row in csvReader: 
            #add this python dict to json array
            jsonArray.append(row)
  
    return jsonArray