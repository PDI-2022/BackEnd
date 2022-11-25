import cv2
import numpy as np
import base64
import csv
from api.services.grid_cut import cortar_malha as cut
from api.services.classification import classificate
from skimage import measure
from shapely.geometry import Polygon
import concurrent.futures
import time

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

def extract_milky_white_percentage(input_image, id=0):
    converted = cv2.cvtColor(input_image, cv2.COLOR_BGR2HSV)
    rgb = np.copy(converted)

    inf_red = 169
    sup_red = 201
    inf_green = 149
    sup_green = 171
    inf_blue = 113
    sup_blue = 144

    for i, line in enumerate(rgb):
        for j, pixel in enumerate(line):
            r, g, b = pixel
            zero_any_channel = False
            if r < inf_red:
                zero_any_channel = True
                rgb[i][j][0] = 0
            if r > sup_red:
                zero_any_channel = True
                rgb[i][j][0] = 0
            if g < inf_green:
                zero_any_channel = True
                rgb[i][j][1] = 0
            if g > sup_green:
                zero_any_channel = True
                rgb[i][j][1] = 0
            if b < inf_blue:
                zero_any_channel = True
                rgb[i][j][2] = 0
            if b > sup_blue:
                zero_any_channel = True
                rgb[i][j][2] = 0
            if zero_any_channel == True:
                rgb[i][j][0] = 0
                rgb[i][j][1] = 0
                rgb[i][j][2] = 0

    pixels_number_seed = np.count_nonzero(input_image)
    pixels_extracted_white = np.count_nonzero(rgb)

    cv2.imwrite(f'./images/white_extract/milky_white_{id}.jpg', cv2.cvtColor(np.hstack([input_image, rgb]), cv2.COLOR_BGR2RGB))

    return pixels_extracted_white/pixels_number_seed

def createCutImgsFold(index):
    externo = cv2.imread(f"./images/background_remove/remove_background_externo{index}.jpg")
    interno = cv2.imread(f"./images/background_remove/remove_background_interno{index}.jpg")

    cv2.imwrite(f'./images/imagens_cortadas/images/semente-' + str(index+1) + '.jpg', np.hstack([externo, interno]))


def extract_seed_information(seed, side, seed_id = 0):
    removed_background = remove_background(seed, f'{side}{seed_id}')
    white_percentage = extract_white_percentage(removed_background, f'{side}{seed_id}')
    milky_white_percentage = extract_milky_white_percentage(removed_background, f'{side}{seed_id}')
    light_red_percentage = extract_light_red_percentage(removed_background, f'{side}{seed_id}')
    dark_red_percentage = extract_dark_red_percentage(removed_background, f'{side}{seed_id}')

    thresholded_red_component = remove_background_and_get_mask(seed)
    (holes, holes_percentage) = count_holes(thresholded_red_component)

    return [
        seed_id + 1,
        side, 
        f'{white_percentage*100:.2f}%',
        f'{milky_white_percentage*100:.2f}%', 
        f'{light_red_percentage*100:.2f}%',
        f'{dark_red_percentage*100:.2f}%',
        holes,
        f'{holes_percentage*100:.2f}%'
    ]


def process_data(intern : str, extern : str, showImgs : bool, showClassification : bool, modelPath : str):
    buffer_intern = base64.b64decode(intern)
    nparr = np.frombuffer(buffer_intern, np.uint8)
    input_intern_image = cv2.imdecode(nparr, flags=1)

    buffer_extern = base64.b64decode(extern)
    nparr = np.frombuffer(buffer_extern, np.uint8)
    input_extern_image = cv2.imdecode(nparr, flags=1)

    intern_seeds = cut(input_intern_image)
    extern_seeds = cut(input_extern_image)

    header = [
        'Semente', 
        'Lado', 
        'Porcentagem de Branco', 
        'Porcentagem de Branco Leitoso',
        'Porcentagem de Vermelho Carmim Claro', 
        'Porcentagem de Vermelho Carmim Escuro', 
        'Quantidade de Buracos', 
        'Área Buraco/Área Semente'
    ]

    if showClassification:
        header.append('Classe')

    rows = []

    start = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = []
        print(f'Número de processos: {executor._max_workers}')
        for i, seed in enumerate(intern_seeds):
            if not is_empty(seed):
                futures.append(
                    executor.submit(extract_seed_information, seed=seed, side='Interno', seed_id=i)
                )

        for i, seed in enumerate(extern_seeds):
            if not is_empty(seed):
                futures.append(
                    executor.submit(extract_seed_information, seed=seed, side='Externo', seed_id=i)
                )

        for future in concurrent.futures.as_completed(futures):
            rows.append(future.result())

    end = time.perf_counter()

    print(f'Imagens processadas em {end-start} segundos')


    # for i, seed in enumerate(intern_seeds):
    #     if not is_empty(seed):
    #         removed_background = remove_background(seed, f'interno{i}')
    #         white_percentage = extract_white_percentage(removed_background, f'interno{i}')
    #         milky_white_percentage = extract_milky_white_percentage(removed_background, f'interno{i}')
    #         light_red_percentage = extract_light_red_percentage(removed_background, f'interno{i}')
    #         dark_red_percentage = extract_dark_red_percentage(removed_background, f'interno{i}')

    #         thresholded_red_component = remove_background_and_get_mask(seed)
    #         (holes, holes_percentage) = count_holes(thresholded_red_component)

    #         rows.append(
    #             [
    #                 i + 1, 
    #                 'Interno', 
    #                 f'{white_percentage*100:.2f}%',
    #                 f'{milky_white_percentage*100:.2f}%', 
    #                 f'{light_red_percentage*100:.2f}%',
    #                 f'{dark_red_percentage*100:.2f}%',
    #                 holes,
    #                 f'{holes_percentage*100:.2f}%'
    #             ]
    #         )        
    # for i, seed in enumerate(extern_seeds):
    #     if not is_empty(seed):
    #         removed_background = remove_background(seed, f'externo{i}')
    #         white_percentage = extract_white_percentage(removed_background, f'externo{i}')
    #         milky_white_percentage = extract_milky_white_percentage(removed_background, f'externo{i}')
    #         light_red_percentage = extract_light_red_percentage(removed_background, f'externo{i}')
    #         dark_red_percentage = extract_dark_red_percentage(removed_background, f'externo{i}')

    #         thresholded_red_component = remove_background_and_get_mask(seed)
    #         (holes, holes_percentage) = count_holes(thresholded_red_component)
    #         createCutImgsFold(i)

    #         rows.append(
    #             [
    #                 i + 1, 
    #                 'Externo', 
    #                 f'{white_percentage*100:.2f}%',
    #                 f'{milky_white_percentage*100:.2f}%', 
    #                 f'{light_red_percentage*100:.2f}%',
    #                 f'{dark_red_percentage*100:.2f}%',
    #                 holes,
    #                 f'{holes_percentage*100:.2f}%'
    #             ]
    #         )

    if showClassification:
        classification = classificate(modelPath)
        classification_number = len(classification)
        for i, row in enumerate(rows):
            row.append(classification[i % classification_number])

    rows.sort(key=lambda value : (0 if value[1] == 'Interno' else 1, value[0]))

    with open('relatorio.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)


    if showImgs:
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