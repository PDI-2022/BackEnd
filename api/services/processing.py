import os
import shutil
import cv2
import numpy as np
import base64
import csv
import uuid
from api.services.detect import deteccao
from api.services.grid_cut import cortar_malha as cut
from api.services.classification import classificate
from skimage import measure
from shapely.geometry import Polygon
import concurrent.futures
import time

from api.services.storage import create_folder,delete_folder
from api.constants.folders import (
    red_extract_folder,
    background_removed_folder,
    white_extract_folder,
    pagination_folder,
    imagens_cortadas_folder,
    embriao_folder,
)


def count_holes(image) -> tuple:
    contours = measure.find_contours(image, 200)

    holes = [Polygon(contour) for contour in contours if len(contour) > 3]

    seed_polygons = []

    # ordenando pela maior área (as duas maiores áreas são os próprio feijão)
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

        return (len(within), (up / down))

    return (0, 0)


def remove_background_and_get_mask(input_image):
    used_threshold, thresholded_bgr_image = cv2.threshold(
        input_image, 110, 255, cv2.THRESH_BINARY
    )
    (
        thresholded_blue_component,
        thresholded_green_component,
        thresholded_red_component,
    ) = cv2.split(thresholded_bgr_image)

    mask_filtered = cv2.medianBlur(thresholded_red_component, 5)

    return mask_filtered


def extract_white_percentage(white_extract_folder_per_id, input_image, id=0):
    hsv = cv2.cvtColor(input_image, cv2.COLOR_BGR2HSV)

    lower = np.array([0, 0, 168])
    upper = np.array([172, 111, 255])
    mask = cv2.inRange(hsv, lower, upper)

    white_extracted_image = cv2.bitwise_and(input_image, input_image, mask=mask)

    pixels_number_seed = np.count_nonzero(input_image)
    pixels_extracted_white = np.count_nonzero(white_extracted_image)

    cv2.imwrite(
        "{0}/white{1}.jpg".format(white_extract_folder_per_id, id),
        np.hstack([input_image, white_extracted_image]),
    )

    return pixels_extracted_white / pixels_number_seed


def remove_background(folder_per_id, input_image, id=0):
    used_threshold, thresholded_bgr_image = cv2.threshold(
        input_image, 110, 255, cv2.THRESH_BINARY
    )
    (
        thresholded_blue_component,
        thresholded_green_component,
        thresholded_red_component,
    ) = cv2.split(thresholded_bgr_image)

    mask_filtered = cv2.medianBlur(thresholded_red_component, 5)

    result_image = cv2.bitwise_and(input_image, input_image, mask=mask_filtered)

    if id != -1:
        cv2.imwrite(
            "{0}/remove_background_{1}.jpg".format(folder_per_id, id),
            result_image,
        )

    return result_image


def extract_dark_red_percentage(
    red_extract_folder_per_id, input_image, lim_inf_red, id=0
):
    hsv = cv2.cvtColor(input_image, cv2.COLOR_BGR2HSV)

    first_lower = np.array([161, lim_inf_red, 80])
    first_upper = np.array([180, 255, 240])
    first_mask = cv2.inRange(hsv, first_lower, first_upper)

    second_lower = np.array([0, lim_inf_red, 80])
    second_upper = np.array([60, 255, 240])
    second_mask = cv2.inRange(hsv, second_lower, second_upper)

    mask = cv2.bitwise_or(first_mask, second_mask)

    dark_red_extracted_image = cv2.bitwise_and(input_image, input_image, mask=mask)

    pixels_number_seed = np.count_nonzero(input_image)
    pixels_extracted_white = np.count_nonzero(dark_red_extracted_image)

    cv2.imwrite(
        "{0}/dark_red_mask{1}.jpg".format(red_extract_folder_per_id, id),
        np.hstack([input_image, dark_red_extracted_image]),
    )

    return pixels_extracted_white / pixels_number_seed


def extract_light_red_percentage(
    light_red_folder_per_id, input_image, lim_sup_red, id=0
):
    hsv = cv2.cvtColor(input_image, cv2.COLOR_BGR2HSV)

    first_lower = np.array([161, 90, 80])
    first_upper = np.array([180, lim_sup_red, 240])
    first_mask = cv2.inRange(hsv, first_lower, first_upper)

    second_lower = np.array([0, 90, 80])
    second_upper = np.array([60, lim_sup_red, 240])
    second_mask = cv2.inRange(hsv, second_lower, second_upper)

    mask = cv2.bitwise_or(first_mask, second_mask)

    light_red_extracted_image = cv2.bitwise_and(input_image, input_image, mask=mask)

    pixels_number_seed = np.count_nonzero(input_image)
    pixels_extracted_white = np.count_nonzero(light_red_extracted_image)

    cv2.imwrite(
        "{0}/light_red_mask_{1}.jpg".format(light_red_folder_per_id, id),
        np.hstack([input_image, light_red_extracted_image]),
    )

    return pixels_extracted_white / pixels_number_seed


def extract_milky_white_percentage(white_extract_folder_per_id, input_image, id=0):
    converted = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)
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

    cv2.imwrite(
        "{0}/milky_white{1}.jpg".format(white_extract_folder_per_id, id),
        cv2.cvtColor(np.hstack([input_image, rgb]), cv2.COLOR_BGR2RGB),
    )

    return pixels_extracted_white / pixels_number_seed


def createCutImgsFold(
    cutted_extract_folder_per_id, background_removed_folder_per_id, index
):
    externo = cv2.imread(
        "{0}/remove_background_externo{1}.jpg".format(
            background_removed_folder_per_id, index
        ),
    )
    interno = cv2.imread(
        "{0}/remove_background_interno{1}.jpg".format(
            background_removed_folder_per_id, index
        ),
    )

    externo = cv2.resize(externo, (300, 256))
    interno = cv2.resize(interno, (300, 256))

    cv2.imwrite(
        "{0}/semente-{1}.jpg".format(cutted_extract_folder_per_id, str(index + 1)),
        np.hstack([externo, interno]),
    )


def extract_seed_information(
    background_removed_folder_per_id,
    white_extract_folder_per_id,
    red_extract_folder_per_id,
    seed,
    side,
    lim_inf_red,
    lim_sup_red,
    seed_id=0,
):
    removed_background = remove_background(
        background_removed_folder_per_id, seed, f"{side}{seed_id}"
    )
    white_percentage = extract_white_percentage(
        white_extract_folder_per_id, seed, f"{side}{seed_id}"
    )
    milky_white_percentage = extract_milky_white_percentage(
        white_extract_folder_per_id, seed, f"{side}{seed_id}"
    )
    light_red_percentage = extract_light_red_percentage(
        red_extract_folder_per_id, seed, lim_sup_red, f"{side}{seed_id}"
    )
    dark_red_percentage = extract_dark_red_percentage(
        red_extract_folder_per_id, seed, lim_inf_red, f"{side}{seed_id}"
    )

    thresholded_red_component = remove_background_and_get_mask(seed)
    (holes, holes_percentage) = count_holes(thresholded_red_component)

    return [
        seed_id + 1,
        side,
        f"{white_percentage*100:.2f}%",
        f"{milky_white_percentage*100:.2f}%",
        f"{light_red_percentage*100:.2f}%",
        f"{dark_red_percentage*100:.2f}%",
        holes,
        f"{holes_percentage*100:.2f}%",
    ]


def decodeImg(img):
    buffer = base64.b64decode(img)
    nparr = np.frombuffer(buffer, np.uint8)
    imgDecoded = cv2.imdecode(nparr, flags=1)
    return imgDecoded


def process_data(
    user_id: int,
    intern: str,
    extern: str,
    showImgs: bool,
    showClassification: bool,
    modelPath: str,
    limInfRed: int,
    limSupRed: int,
    imgJoined: bool,
    model,
    embriao_model,
    classificationYolo: bool,
    seedsClassNumberInput: int,
):

    # Transforma as imagens de base64 para buffer
    input_intern_image = decodeImg(intern)
    input_extern_image = decodeImg(extern)

    # Corta as imagens
    intern_seeds = cut(input_intern_image, imgJoined)
    extern_seeds = cut(input_extern_image, imgJoined)

    # Gera as pastas para armazenamento dos imagens processadas
    red_extract_folder_per_id = "users_folders_imgs/{}{}".format(
        user_id, red_extract_folder
    )
    background_removed_folder_per_id = "users_folders_imgs/{}{}".format(
        user_id, background_removed_folder
    )
    embriao_extract_folder_per_id = "users_folders_imgs/{}{}".format(
        user_id, embriao_folder
    )
    white_extract_folder_per_id = "users_folders_imgs/{}{}".format(
        user_id, white_extract_folder
    )
    pagination_folder_per_id = "users_folders_imgs/{}{}".format(
        user_id, pagination_folder
    )
    cutted_extract_folder_per_id = "users_folders_imgs/{}{}".format(
        user_id, imagens_cortadas_folder
    )
    #deleta as pastas
    delete_folder(f"./users_folders_imgs/{user_id}")

    # cria as pastas a serem usadas pela aplicação.
    create_folder(red_extract_folder_per_id)
    create_folder(background_removed_folder_per_id)
    create_folder(embriao_extract_folder_per_id)
    create_folder(white_extract_folder_per_id)
    create_folder(pagination_folder_per_id)
    create_folder(cutted_extract_folder_per_id)

    if showImgs:
        if os.path.exists(pagination_folder_per_id):
            shutil.rmtree(pagination_folder_per_id)
        create_folder(pagination_folder_per_id)
        for id, int_seed in enumerate(intern_seeds):
            cv2.imwrite(f"{pagination_folder_per_id}/Internal_seed_{id}.jpg", int_seed)

        for id, ext_seed in enumerate(extern_seeds):
            cv2.imwrite(f"{pagination_folder_per_id}/External_seed_{id}.jpg", ext_seed)

    # Gera o header do csv
    header = [
        "Semente",
        "Lado",
        "Porcentagem de Branco",
        "Porcentagem de Branco Leitoso",
        "Porcentagem de Vermelho Carmim Claro",
        "Porcentagem de Vermelho Carmim Escuro",
        "Quantidade de Buracos",
        "Área Buraco/Área Semente",
    ]

    if showClassification:
        header.append("Classe")

    rows = []

    # Extrai as informações da parte externa e interna das sementes
    start = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = []
        print(f"Número de processos: {executor._max_workers}")
        for i, seed in enumerate(intern_seeds):
            if not is_empty(background_removed_folder_per_id, seed):
                futures.append(
                    executor.submit(
                        extract_seed_information,
                        background_removed_folder_per_id=background_removed_folder_per_id,
                        white_extract_folder_per_id=white_extract_folder_per_id,
                        red_extract_folder_per_id=red_extract_folder_per_id,
                        seed=seed,
                        side="interno",
                        lim_inf_red=limInfRed,
                        lim_sup_red=limSupRed,
                        seed_id=i,
                    )
                )

        for i, seed in enumerate(extern_seeds):
            if not is_empty(background_removed_folder_per_id, seed):
                futures.append(
                    executor.submit(
                        extract_seed_information,
                        background_removed_folder_per_id=background_removed_folder_per_id,
                        white_extract_folder_per_id=white_extract_folder_per_id,
                        red_extract_folder_per_id=red_extract_folder_per_id,
                        seed=seed,
                        side="externo",
                        lim_inf_red=limInfRed,
                        lim_sup_red=limSupRed,
                        seed_id=i,
                    )
                )

        for future in concurrent.futures.as_completed(futures):
            rows.append(future.result())

    end = time.perf_counter()

    print(f"Imagens processadas em {end-start} segundos")

    if showClassification or classificationYolo:
        for i in range(len(extern_seeds)):
            createCutImgsFold(
                cutted_extract_folder_per_id, background_removed_folder_per_id, i
            )

    # Faz a detecção do embrião
    if classificationYolo:
        create_folder(embriao_extract_folder_per_id)
        for i in range(len(extern_seeds)):
            path = f"./users_folders_imgs/{user_id}/images/imagens_cortadas/images/semente-{i+1}.jpg"
            img = cv2.imread(path)

            deteccao(embriao_extract_folder_per_id, embriao_model, img, i)

    rows.sort(key=lambda value: (0 if value[1] == "Interno" else 1, value[0]))

    # Classifica as sementes e gera a parte correspondente no csv
    classes = int(seedsClassNumberInput)
    if showClassification:
        classification = classificate(
            cutted_extract_folder_per_id, model, modelPath, classes
        )
        index = 0
        for i, row in enumerate(rows):
            row.append(classification[index])
            if ((i + 1) % 2) == 0:
                index = index + 1

        class_counters = [0, 0, 0, 0, 0, 0, 0]
        total = len(classification)
        for clazz in classification:
            class_counters[int(clazz) - 1] += 1

        class_percentage = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        for i in range(7):
            class_percentage[i] = class_counters[i] / total

        vigor = (class_counters[0] + class_counters[1] + class_counters[2]) / total
        viability = (
            class_counters[0]
            + class_counters[1]
            + class_counters[2]
            + class_counters[3]
            + class_counters[4]
        ) / total

        rows.append([])
        rows.append(
            [
                "Vigor",
                "Viabilidade",
                "% Classe 1",
                "% Classe 2",
                "% Classe 3",
                "% Classe 4",
                "% Classe 5",
                "% Classe 6",
                "% Classe 7",
            ]
        )
        rows.append(
            [
                f"{vigor*100:.2f}%",
                f"{viability*100:.2f}%",
                f"{class_percentage[0]*100:.2f}%",
                f"{class_percentage[1]*100:.2f}%",
                f"{class_percentage[2]*100:.2f}%",
                f"{class_percentage[3]*100:.2f}%",
                f"{class_percentage[4]*100:.2f}%",
                f"{class_percentage[5]*100:.2f}%",
                f"{class_percentage[6]*100:.2f}%",
            ]
        )

    folder = "./relatorios/{}".format(user_id)
    create_folder(folder)
    csv_report_file_name = "./relatorios/{}/{}_{}.csv".format(
        user_id, "relatorio", str(uuid.uuid4())
    )
    with open(csv_report_file_name, "w+", encoding="UTF8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)

    return csv_report_file_name


def is_empty(folder_per_id, block):
    removed_background = remove_background(folder_per_id, block, -1)
    percentage = np.count_nonzero(removed_background) / (
        block.shape[0] * block.shape[1]
    )

    return True if percentage < 0.05 else False


def extract_embriao_information(
    folder_per_id, embriao, lim_inf_red, lim_sup_red, seed_id=0
):
    white_percentage = extract_white_percentage(
        folder_per_id, embriao, f"embriao{seed_id}"
    )
    milky_white_percentage = extract_milky_white_percentage(
        folder_per_id, embriao, f"embriao{seed_id}"
    )
    light_red_percentage = extract_light_red_percentage(
        folder_per_id, embriao, lim_sup_red, f"embriao{seed_id}"
    )
    dark_red_percentage = extract_dark_red_percentage(
        folder_per_id, embriao, lim_inf_red, f"embriao{seed_id}"
    )

    return [
        seed_id,
        f"{white_percentage*100:.2f}%",
        f"{milky_white_percentage*100:.2f}%",
        f"{light_red_percentage*100:.2f}%",
        f"{dark_red_percentage*100:.2f}%",
    ]


def process_embriao(
    embriao_folder_per_id, user_id, embrioes, limInfRed=168, limSupRed=190
):

    header = [
        "Semente",
        "Porcentagem de branco",
        "Porcentagem de branco leitoso",
        "Porcentagem de vermelho claro",
        "Porcentagem de vermelho escuro",
    ]

    rows = []

    start = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = []
        print(f"Número de processos: {executor._max_workers}")
        for i, seed in embrioes:
            if not is_empty(embriao_folder_per_id, seed):
                futures.append(
                    executor.submit(
                        extract_embriao_information,
                        folder_per_id=embriao_folder_per_id,
                        embriao=seed,
                        lim_inf_red=limInfRed,
                        lim_sup_red=limSupRed,
                        seed_id=i,
                    )
                )

        for future in concurrent.futures.as_completed(futures):
            rows.append(future.result())

    end = time.perf_counter()
    print(f"Tempo de processamento dos embriões: {end - start}")
    rows.sort(key=lambda value: int(value[0]))

    folder = "./relatorios/{}".format(user_id)
    create_folder(folder)
    csv_report_file_name = "{}/{}_{}.csv".format(
        folder, "relatorio_embriao", str(uuid.uuid4())
    )

    with open(csv_report_file_name, "w+", encoding="UTF8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)

    return csv_report_file_name
