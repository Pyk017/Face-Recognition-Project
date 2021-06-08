import cv2
import numpy as np
import pickle
import shutil
from os import path, walk, makedirs, getcwd, walk, scandir
from final_project.settings import BASE_DIR

class Recognize:
    def recognize(self):
        face_classifier = cv2.CascadeClassifier(str(BASE_DIR) + '\\fr\\haarcascade_frontalface_default.xml')
        recognizer_lbph = cv2.face.LBPHFaceRecognizer_create()
        recognizer_lbph.read(str(BASE_DIR) + "\\fr\\trainner.yml")

        labels = {}
        with open(str(BASE_DIR) + '\\labels\\face-labels.pickle', 'rb') as file:
            org_labels = pickle.load(file)
            labels = {v: k for k, v in org_labels.items()}

        cap = cv2.VideoCapture(0)
        username = ''
        while True:
            retval, frame = cap.read()
            # Face detection
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cap_face = face_classifier.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

            for (x, y, w, h) in cap_face:
                roi_gray = gray_frame[y:y + h, x:x + h]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                # Recognition based on trained model
                id_, confidence = recognizer_lbph.predict(roi_gray)
                confidence = int(100 * (1 - (confidence / 300)))
                #if face is recognized
                if confidence > 80:
                    name = labels[id_]
                    cv2.putText(frame, str(name) + ' ' + str(confidence) + '%', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                    username = str(name)
                    #return username of recognized user
                    return username
                #if face is not recognized then
                else:
                    cv2.putText(frame, 'unknown', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                    return username

            cv2.imshow('frame', frame)
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        return username




class Training:
    def labels_for_training_data(self):
        current_id = 0
        label_ids = dict()
        faces, faces_ids = list(), list()

        # Go through directories and find label and path to image
        for root, dirs, files in walk(str(BASE_DIR) + '\\data'):
            for file in files:
                if file.endswith('.jpg') or file.endswith('.png'):
                    img_path = path.join(root, file)
                    label = path.basename(root).replace(' ', '-').lower()
                    if label not in label_ids:
                        label_ids[label] = current_id
                        current_id += 1
                    id_ = label_ids[label]

                    test_img = cv2.imread(img_path)
                    test_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
                    if test_img is None:
                        print('Image not loaded properly')
                        continue

                    faces.append(test_img)
                    faces_ids.append(id_)

        # Make directory with labels doesn't exist make directory and file with labels
        # print(path.exists(str(BASE_DIR) + 'labels\\'))
        if not path.exists(str(BASE_DIR) + 'labels\\'):
            makedirs('labels\\')
        with open(str(BASE_DIR) + '\\labels\\face-labels.pickle', 'wb') as file:
            pickle.dump(label_ids, file)

        return faces, faces_ids


    
    def train_classifier(self, train_faces, train_faces_ids):
        """Function train model to recognize face with local binary pattern histogram algorithm"""
        recognizer_lbph = cv2.face.LBPHFaceRecognizer_create()
        print('Training model in progress...')
        recognizer_lbph.train(train_faces, np.array(train_faces_ids))
        print('Saving...')
        recognizer_lbph.save(str(BASE_DIR) + '\\fr\\trainner.yml')
        print('Model training complete!')


class Capture(Training, Recognize):
    #face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    def __init__(self):
        # print(str(BASE_DIR))
        self.face_classifier = cv2.CascadeClassifier(str(BASE_DIR) + '\\fr\\haarcascade_frontalface_default.xml')
        # print('Enter username: ', end='')
        self.directory = ''
        self.username = self.directory
        self.currDirectory = getcwd()
        # if not path.exists(str(BASE_DIR) + '\\data\\' + str(self.directory.lower())):
        #     makedirs(str(BASE_DIR) + '\\data\\' + str(self.directory.lower()))
            

    
    def face_extractor(self, cap_frame):
        """Function detect face and return region of interest"""
        gray_frame = cv2.cvtColor(cap_frame, cv2.COLOR_BGR2GRAY)
        cap_face = self.face_classifier.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in cap_face:
            roi = cap_frame[y:y + h, x:x + w]
            return roi


    def deleteTheDirectory(self):
        flag = False
        for dirpath, dirnames, filenames in walk(self.currDirectory):
            for x in dirnames:
                if x == self.username:
                    result = dirpath
                    flag = True
                    break
            if flag:
                break
        #print(result)

        for f in scandir(result):
            if f.is_dir() and f.name == self.username:
                final = f.path
                break
        
        #print(final)
        shutil.rmtree(final)
        

    def invokeTraining(self):
        faces, face_ids = self.labels_for_training_data()
        self.train_classifier(faces, face_ids)
    
        

    def takePhotos(self, data):
        self.directory = data
        self.username = self.directory

        if not path.exists(str(BASE_DIR) + '\\data\\' + str(self.directory.lower())):
            makedirs(str(BASE_DIR) + '\\data\\' + str(self.directory.lower()))

        cap = cv2.VideoCapture(0)
        count = 0
        not_found = 0

        while True:
            ret, frame = cap.read()
            if self.face_extractor(frame) is not None:
                face = cv2.resize(self.face_extractor(frame), (200, 200))
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

                # If face was detected save region of interest in user directory
                file_name_path = str(BASE_DIR) + '\\data\\'+str(self.directory.lower())+'\\'+str(count)+'.jpg'
                # str(BASE_DIR) +'\\fr\\dataset\\User.' + str(face_id) + '.' + str(count) + ".jpg"
                print(file_name_path)
                res = cv2.imwrite(file_name_path, face)
                print('imwrite', res)
                count += 1

                # Print number of already saved samples
                cv2.putText(face, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, 200, 2)
                cv2.imshow('Collecting samples', face)
            else:
                #print('Face not found')
                not_found += 1

            if cv2.waitKey(30) & 0xFF == ord('q') or count == 50:
                break

        cap.release()
        cv2.destroyAllWindows()
        #print('Collecting samples complete!')
        #print(count)
        # if images without face are <= 5 out of total 15 images train the data else 
        if not_found <= 5:
            return True
        else:
            return False



# c = Capture()
# result = c.takePhotos()
# if not result:
#     c.deleteTheDirectory()
#     print("take the photos again")
# else:
#     c.invokeTraining()
#     user = c.recognize()
#     if len(user) == 0:
#         print("Not allowed")
#     else:
#         print(user)



'''
r = Recognize()
user = r.recognize()
if len(user) == 0:
    print("not allowed")
else:
    print(user)
'''


#Steps to run from signup using Capture:
        
# 1) Object of Capture --> created username and userdirectory in data folder. 
# 2) call the takePhotos method --> take 15 sample pictures of the user and check if there are atleast 10 photos that are completely accurate.
#    if True : training, else : then delete the user folder from data directory by caling the method deleteTheDirectory using Capture object and show the user the message to take photos again ie. takePhotos called again and
# 3) If there are atleast 10 photos then we move on to training ie. the condition is true, then we invoke invokeTraining method in Capture class.
# 4) Then we call the recogize method in Recognize class to recognize the face. If True print the name of the user otherwise the user is not allowed. 
# 5) All this is done using the object of the Capture class.


    
#Steps to run from login using Recognize:

# 1) make an object of the Recognize class --> it will just check for the procedure of recognition
# 2) if an empty string is returned then the user is not authenticated ie. show the message not allowed
# 3) Otherwise direct the user to the profile page.






