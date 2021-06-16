def format_pytesseract_dict_results(ocr_res: dict) -> tuple:
    """Formats results from pytesseract.image_to_data(img, output_type=Output.DICT)
    function.

    Parameters
    ----------
    ocr_res : dict
        result of pytesseract.image_to_data(img, output_type=Output.DICT)

    Returns
    -------
    tuple(list):
        paragraphs: list of strings of paragraphs detected
        bboxes: list for (x1,y1,w,h) for each paragraphs
        
    """
    paragraphs = []
    bboxes = []

    for b in set(ocr_res['block_num']):
        par_nums = set([p for (i, p) in enumerate(ocr_res['par_num']) if ocr_res['block_num'][i] == b])

        x1 = 100000
        y1 = 100000
        x2 = -1
        y2 = -1

        res = ''
        for p in par_nums:
            par_content = {k: [x for i, x in enumerate(v) 
                               if (ocr_res['block_num'][i] == b) and (ocr_res['par_num'][i] == p)] 
                           for k, v in ocr_res.items()}

            cur_line = 0
            for i in range(len(par_content['text'])):
                line_num = par_content['line_num'][i]
                txt = par_content['text'][i]
                x = par_content['left'][i]
                y = par_content['top'][i]
                w = par_content['width'][i]
                h = par_content['height'][i]

                if line_num != cur_line:
                    cur_line = line_num

                if txt.strip() == '':
                    continue

                x1 = x if x < x1 else x1
                y1 = y if y < y1 else y1
                x2 = x+w if x+w > x2 else x2
                y2 = y+h if y+h > y2 else y2

                res += txt + ' '

        if res == '':
            continue

        paragraphs.append(res)
        w = x2 - x1
        h = y2 - y1
        bboxes.append((x1,y1,w,h))

    return paragraphs, bboxes