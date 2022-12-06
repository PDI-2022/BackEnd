import os
import shutil
import cv2
import numpy as np
import base64
import csv
from api.services.detect import deteccao
from api.services.grid_cut import cortar_malha as cut
from api.services.classification import classificate
from skimage import measure
from shapely.geometry import Polygon
import concurrent.futures
import time
from api.constants.folders import pagination_folder

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

    if id != -1:
        cv2.imwrite(f'./images/background_remove/remove_background_{id}.jpg', result_image)

    return result_image

def extract_dark_red_percentage(input_image, lim_inf_red, id=0):
    hsv = cv2.cvtColor(input_image, cv2.COLOR_BGR2HSV)
    
    first_lower = np.array([161, lim_inf_red, 80])
    first_upper = np.array([180 , 255, 240])   
    first_mask = cv2.inRange(hsv, first_lower, first_upper)

    second_lower = np.array([0, lim_inf_red, 80])
    second_upper = np.array([60 , 255, 240])   
    second_mask = cv2.inRange(hsv, second_lower, second_upper)

    mask = cv2.bitwise_or(first_mask, second_mask)

    dark_red_extracted_image = cv2.bitwise_and(input_image, input_image, mask = mask)

    pixels_number_seed = np.count_nonzero(input_image)
    pixels_extracted_white = np.count_nonzero(dark_red_extracted_image)

    cv2.imwrite(f'./images/red_extract/dark_red_mask{id}.jpg', np.hstack([input_image, dark_red_extracted_image]))

    return pixels_extracted_white/pixels_number_seed

def extract_light_red_percentage(input_image, lim_sup_red, id=0):
    hsv = cv2.cvtColor(input_image, cv2.COLOR_BGR2HSV)

    first_lower = np.array([161, 90, 80])
    first_upper = np.array([180 , lim_sup_red, 240])   
    first_mask = cv2.inRange(hsv, first_lower, first_upper)

    second_lower = np.array([0, 90, 80])
    second_upper = np.array([60 , lim_sup_red, 240])   
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
    sup_red = 220
    inf_green = 135
    sup_green = 190
    inf_blue = 105
    sup_blue = 150

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

    externo = cv2.resize(externo, (300, 256))
    interno = cv2.resize(interno, (300, 256))

    cv2.imwrite(f'./images/imagens_cortadas/images/semente-' + str(index+1) + '.jpg', np.hstack([externo, interno]))


def extract_seed_information(seed, side, lim_inf_red, lim_sup_red, seed_id = 0 ):
    removed_background = remove_background(seed, f'{side}{seed_id}')
    white_percentage = extract_white_percentage(removed_background, f'{side}{seed_id}')
    milky_white_percentage = extract_milky_white_percentage(removed_background, f'{side}{seed_id}')
    light_red_percentage = extract_light_red_percentage(removed_background, lim_sup_red, f'{side}{seed_id}')
    dark_red_percentage = extract_dark_red_percentage(removed_background, lim_inf_red, f'{side}{seed_id}')

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


def process_data(
    intern : str, 
    extern : str, 
    showImgs : bool, 
    showClassification : bool, 
    modelPath : str, 
    limInfRed : int, 
    limSupRed: int,
    imgJoined: bool,
    model,
    embriao_model,
    classificationYolo:bool    
):
    buffer_intern = base64.b64decode(intern)
    nparr = np.frombuffer(buffer_intern, np.uint8)
    input_intern_image = cv2.imdecode(nparr, flags=1)

    buffer_extern = base64.b64decode(extern)
    nparr = np.frombuffer(buffer_extern, np.uint8)
    input_extern_image = cv2.imdecode(nparr, flags=1)

    intern_seeds = cut(input_intern_image,imgJoined)
    extern_seeds = cut(input_extern_image,imgJoined)
    
    if os.path.exists(pagination_folder):
        shutil.rmtree(pagination_folder)
    os.makedirs(pagination_folder)
    for id, int_seed in enumerate(intern_seeds):
        cv2.imwrite(f'{pagination_folder}/Internal_seed_{id}.jpg', int_seed)

    for id, ext_seed in enumerate(extern_seeds):
        cv2.imwrite(f'{pagination_folder}/External_seed_{id}.jpg', ext_seed)

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
                    executor.submit(
                        extract_seed_information, 
                        seed=seed, 
                        side='interno', 
                        lim_inf_red=limInfRed, 
                        lim_sup_red=limSupRed, 
                        seed_id=i
                    )
                )

        for i, seed in enumerate(extern_seeds):
            if not is_empty(seed):
                futures.append(
                    executor.submit(
                        extract_seed_information, 
                        seed=seed, 
                        side='externo',
                        lim_inf_red=limInfRed,
                        lim_sup_red=limSupRed,
                        seed_id=i
                    )
                )

        for future in concurrent.futures.as_completed(futures):
            rows.append(future.result())

    end = time.perf_counter()

    print(f'Imagens processadas em {end-start} segundos')
    if classificationYolo:
        for i in range(len(extern_seeds)):
            path=f"./images/imagens_cortadas/images/semente-{i+1}.jpg"
            img = cv2.imread(path)
            deteccao(embriao_model, img,i)

    rows.sort(key=lambda value : (0 if value[1] == 'Interno' else 1, value[0]))
    classes = 7
    if showClassification:
        for i in range(len(extern_seeds)):
            print(i)
            createCutImgsFold(i)

        classification = classificate(model, modelPath, classes)
        index = 0
        for i, row in enumerate(rows):
            row.append(classification[index])
            if(((i+1) % 2) == 0):
                index = index + 1

        class_counters = [0, 0, 0, 0, 0, 0, 0]
        total = len(classification)
        for clazz in classification:
            class_counters[int(clazz) - 1] += 1
        
        class_percentage = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        for i in range(7):
            class_percentage[i] = (class_counters[i] / total)

        vigor = (class_counters[0] + class_counters[1] + class_counters[2]) / total
        viability = (class_counters[0] + class_counters[1] + class_counters[2] + class_counters[3] + class_counters[4]) / total

        rows.append([])
        rows.append(['Vigor', 'Viabilidade', '% Classe 1', '% Classe 2', '% Classe 3', '% Classe 4', '% Classe 5', '% Classe 6', '% Classe 7'])
        rows.append([
            f'{vigor*100:.2f}%', 
            f'{viability*100:.2f}%', 
            f'{class_percentage[0]*100:.2f}%',
            f'{class_percentage[1]*100:.2f}%',
            f'{class_percentage[2]*100:.2f}%',
            f'{class_percentage[3]*100:.2f}%',
            f'{class_percentage[4]*100:.2f}%',
            f'{class_percentage[5]*100:.2f}%',
            f'{class_percentage[6]*100:.2f}%',
            ])

    with open('relatorio.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)


    if showImgs:
        return GenImg(intern_seeds,extern_seeds)

    return 'relatorio.csv'


def is_empty(block):
    removed_background = remove_background(block, -1)
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

def extract_embriao_information(embriao, lim_inf_red, lim_sup_red, seed_id = 0 ):
    white_percentage = extract_white_percentage(embriao, f'embriao{seed_id}')
    milky_white_percentage = extract_milky_white_percentage(embriao, f'embriao{seed_id}')
    light_red_percentage = extract_light_red_percentage(embriao, lim_sup_red, f'embriao{seed_id}')
    dark_red_percentage = extract_dark_red_percentage(embriao, lim_inf_red, f'embriao{seed_id}')

    return [
        seed_id,
        f'{white_percentage*100:.2f}%',
        f'{milky_white_percentage*100:.2f}%', 
        f'{light_red_percentage*100:.2f}%',
        f'{dark_red_percentage*100:.2f}%'
    ]

def process_embriao(embrioes, limInfRed=168, limSupRed=190):

    header = [
        'Semente', 
        'Porcentagem de branco', 
        'Porcentagem de branco leitoso',
        'Porcentagem de vermelho claro',
        'Porcentagem de vermelho escuro'
    ]

    rows = []

    start = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = []
        print(f'Número de processos: {executor._max_workers}')
        for i, seed in embrioes:
            if not is_empty(seed):
                futures.append(
                    executor.submit(
                        extract_embriao_information, 
                        embriao=seed, 
                        lim_inf_red=limInfRed, 
                        lim_sup_red=limSupRed, 
                        seed_id=i
                    )
                )

        for future in concurrent.futures.as_completed(futures):
            rows.append(future.result())

    end = time.perf_counter()

    print(f'Tempo de processamento dos embriões: {end - start}')

    rows.sort(key=lambda value : int(value[0]))

    with open('relatorio_embriao.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)

    return 'relatorio_embriao.csv'
