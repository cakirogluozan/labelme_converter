import os
import xml.etree.ElementTree as ET
import cv2

def str2int(x1,y1,x2,y2):
    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)

    return x1,y1,x2,y2

def main():

    LABELED_DIR = 'object_list'
    folders = os.listdir(LABELED_DIR)
    print(folders)
    DATASET_DIR  = 'data'

    if not os.path.exists(DATASET_DIR):
       os.mkdir(DATASET_DIR)


    for folder in folders:
        negatives = folders.copy()
        negatives.remove(folder)
        negative_file = open('negative_{}.txt'.format(folder), 'w')

        for negative in negatives:
            FOLDER_DIR = os.path.join(LABELED_DIR, negative)
            XML_DIR    = os.path.join(FOLDER_DIR, 'Annotations/users/iremonur/{}'.format(negative))
            IMAGE_DIR = os.path.join(DATASET_DIR, negative)

            if not os.path.exists(IMAGE_DIR):
                os.mkdir(IMAGE_DIR)

            for neg_xml in os.listdir(XML_DIR):
                jpg_name   = neg_xml.split('.')[0] + '.jpg'
                line       = os.path.join(IMAGE_DIR, jpg_name) 
                negative_file.write(line + '\n')
    
        negative_file.close()

        positive_file = open('positive_{}.txt'.format(folder), 'w')

        FOLDER_DIR = os.path.join(LABELED_DIR, folder)
        XML_DIR    = os.path.join(FOLDER_DIR, 'Annotations/users/iremonur/{}'.format(folder))
        IMAGE_DIR = os.path.join(DATASET_DIR, folder)
        LABELED_IMAGE_DIR = os.path.join(FOLDER_DIR, 'Images/users/iremonur/{}'.format(folder))

        if not os.path.exists(IMAGE_DIR):
            os.mkdir(IMAGE_DIR)

        for xml in sorted(os.listdir(XML_DIR)):

            xml_file = os.path.join(XML_DIR, xml)
            if xml == 'image304.xml' and folder == 'stop_s':
                break
            print(xml_file)
            tree     = ET.parse(xml_file)
            root     = tree.getroot()
            objects  = root.findall("./object")

            if objects is None:
                continue

            for ind, object_ in enumerate(objects):
                deleted_flag = object_.find('./deleted').text
                if deleted_flag != '0':
                    continue

                polygon    = object_.find('./polygon')
                left_top   = polygon[1]
                bot_right  = polygon[3]

                x1, y1     = left_top[0].text, left_top[1].text
                x2, y2     = bot_right[0].text, bot_right[1].text

                jpg_name   = xml.split('.')[0] + '.jpg'
                class_     = folder
                processed_image_name = os.path.join(IMAGE_DIR, jpg_name)

                labeled_image_name = os.path.join(LABELED_IMAGE_DIR, jpg_name) 
                frame = cv2.imread(labeled_image_name)

                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                subframe = frame[y1:y2, x1:x2]
                resized_subframe = cv2.resize(subframe, (64, 64))
                cv2.imwrite(processed_image_name, resized_subframe)

                new_x, new_y, new_w, new_h = "0", "0", "64", "64" 
                line = '{} {} {} {} {} {}\n'.format(processed_image_name, 1, new_x, new_y, new_w, new_h)
                positive_file.write(line)
                        
        positive_file.close()

if __name__ == "__main__":
    print('post processing has been started')
    main()
