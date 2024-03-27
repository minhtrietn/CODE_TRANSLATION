import runpy

try:
    runpy.run_module("check_version")
except Exception:
    ...
# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************
# **********************************************************************************************************************
print("VUI LÒNG ĐỢI CHƯƠNG TRÌNH KHỞI CHẠY!")
try:
    from asset.Dictionary.Button import *
    from asset.Dictionary.pygametextboxinput import *
    from asset.Dictionary.pygame_imslider import *
    from pygame_widgets.slider import Slider
    from tkinter.filedialog import askopenfilename
    from math import degrees, atan2
    import tkinter as tk
    import pygame_widgets
    import json
    import time
    import pygame
    import pyttsx3
    import sounddevice
    import numpy as np
    import mediapipe as mp
    import cv2

except ModuleNotFoundError:
    import os

    print("ĐANG TIẾN HÀNH CÀI ĐẶT THƯ VIỆN")
    os.system("setup.bat")
    try:
        from asset.Dictionary.Button import *
        from asset.Dictionary.pygametextboxinput import *
        from asset.Dictionary.pygame_imslider import *
        from pygame_widgets.slider import Slider
        from tkinter.filedialog import askopenfilename
        from math import degrees, atan2
        import tkinter as tk
        import pygame_widgets
        import json
        import time
        import pygame
        import pyttsx3
        import sounddevice
        import numpy as np
        import mediapipe as mp
        import cv2

    except ModuleNotFoundError:
        os.system("python GUI.py")
        os.system("exit")

    print("ĐÃ HOÀN THÀNH VIỆC CÀI ĐẶT THƯ VIỆN!")

# Tạo GUI
pygame.init()
surface_screen = pygame.display.set_mode((1100, 600))

pygame.scrap.init()
pygame.scrap.set_mode(pygame.SCRAP_CLIPBOARD)

# Tên và icon
image_icon = pygame.image.load("asset\\Image\\icon.png").convert_alpha()
pygame.display.set_caption('CODE TRANSLATIONS')
pygame.display.set_icon(image_icon)

root = tk.Tk()
root.withdraw()
image_icon_tk = tk.PhotoImage(file="asset\\Image\\icon.png")
root.iconphoto(False, image_icon_tk)


# Hàm hỗ trợ
def help_menu():
    ...


def help_options():
    ...


def help_MORSE():
    ...


def help_SEMAPHORE():
    ...


def help_OpenCV_surface():
    ...


def effect_clicked():
    global bool_check_effect
    if bool_check_effect:
        try:
            sound_click_sfx.play()
        except Exception:
            ...


# Hàm chế độ MORSE
def MORSE():
    global fps, bool_morse_clicked, bool_status_mod, bool_value_error, dic_morse_to_text, dic_text_to_morse, temp_pos1, temp_pos2, text_Morse_surface, text_Document_surface, bool_morse_setting_clicked, text_temp2, text_temp1, string_input, int_check_starter

    clock.tick(fps)

    surface_screen.fill((25, 25, 25))

    surface_screen.blit(text_MORSE_title, (446.5, 20))

    text_box.update(events)
    text_box.render(surface_screen, (41, 41, 41))
    text_box.set_text_note("Your text here...")

    text_box2.update(events)
    text_box2.render(surface_screen, (41, 41, 41))

    if surface_button_change.draw(surface_screen):
        effect_clicked()
        bool_status_mod = not bool_status_mod
        change_mod()

    text_Document_surface = surface_screen.blit(text_Document, (temp_pos1, 150))
    text_Morse_surface = surface_screen.blit(text_Morse, (temp_pos2, 150))

    if surface_button_copy.draw(surface_screen):
        effect_clicked()
        pygame.scrap.put(pygame.SCRAP_TEXT, text_box2.get_text().encode())

    if surface_button_speaker.draw(surface_screen):
        effect_clicked()
        if not bool_status_mod:
            engine = pyttsx3.init()
            engine.say(text_box2.get_text())
            engine.runAndWait()
        else:
            play_morse_code(text_box2.get_text(), slider_morse_sound_setting.getValue() / 100)

    if surface_button_upload.draw(surface_screen):
        effect_clicked()
        filename = askopenfilename()

        if filename[-4:] == ".txt":
            string_filename = ""
            for i in open(filename, "r").readlines():
                string_filename += i
            text_box.set_text(string_filename)
        elif filename[-4:] == "":
            pass
        else:
            bool_value_error = True
            int_check_starter = 1

    if surface_back_button.draw(surface_screen):
        effect_clicked()
        bool_morse_clicked = False

    if surface_button_setting.draw(surface_screen):
        effect_clicked()
        if bool_morse_setting_clicked:
            bool_morse_setting_clicked = False
        else:
            bool_morse_setting_clicked = True

    if bool_value_error:
        value_error_gui()
    else:
        int_check_starter = 0

    if not bool_status_mod:
        if text_box_dot.get_text() == "" and text_box_.get_text() == "":
            string_input = text_box.get_text()
        else:
            if text_box_dot.get_text() != "":
                string_input = text_box.get_text().replace(text_box_dot.get_text(), ".")
            if text_box_.get_text() != "":
                string_input = string_input.replace(text_box_.get_text(), "-")
        word = string_input.replace("\n", " \n ")
        if string_input == "":
            text_box2.set_text("")
        word = word.split(" ")
        text = ""
        for i in word:
            try:
                text += dic_morse_to_text[i]
                text_box2.set_text(text)
            except KeyError:
                if i == "\n":
                    text += "\n"
                elif i == "":
                    pass
                else:
                    text += "#"
                text_box2.set_text(text)
    else:
        if text_box_dot.get_text() == "" and text_box_.get_text() == "":
            string_input = text_box.get_text().upper()
        else:
            if text_box_dot.get_text() != "":
                string_input = text_box.get_text().upper().replace(text_box_dot.get_text(), ".")
            if text_box_.get_text() != "":
                string_input = string_input.replace(text_box_.get_text(), "-")
        text = ""
        if string_input == "":
            text_box2.set_text("")
        for i in string_input:
            try:
                text += dic_text_to_morse[i] + " "
                text_box2.set_text(text)
            except KeyError:
                if i == "\n":
                    text = text[:-1]
                    text += "\n"
                else:
                    text += "# "
                    text_box2.set_text(text)

    if bool_morse_setting_clicked:
        morse_setting()
        text_box.status = False
    else:
        text_box.status = True


def change_mod():
    global text_temp1, text_temp2, temp_pos1, temp_pos2
    if text_box_dot.get_text() == "" and text_box_.get_text() == "":
        text_temp1 = text_box.get_text()
        text_temp2 = text_box2.get_text()
    else:
        if text_box_dot.get_text() != "":
            text_temp1 = text_box.get_text().replace(text_box_dot.get_text(), ".")
            text_temp2 = text_box2.get_text().replace(text_box_dot.get_text(), ".")
        if text_box_.get_text() != "":
            text_temp1 = text_temp1.replace(text_box_.get_text(), "-")
            text_temp2 = text_temp2.replace(text_box_.get_text(), "-")
    temp_pos1 = text_Morse_surface.x
    temp_pos2 = text_Document_surface.x

    text_box.set_text(text_temp2)
    text_box2.set_text(text_temp1)

    text_Morse_surface.x = temp_pos2
    text_Document_surface.x = temp_pos1


def value_error_gui():
    global bool_value_error, int_check_starter, int_time_start, mouse_pos
    surface_screen_value_error = pygame.Surface((750, 400)).convert_alpha()
    surface_screen_value_error.fill((37, 37, 37))
    surface_screen_value_error.set_alpha(230)
    surface_screen.blit(surface_screen_value_error, (175, 100))

    surface_screen.blit(image_warning, (200, 237.5))
    surface_screen.blit(text_value_error, (345, 269.5))

    pos_value_error = (175, 100)
    rect_value_error = pygame.rect.Rect(pos_value_error + surface_screen_value_error.get_size())

    if not rect_value_error.collidepoint(mouse_pos):
        if pygame.mouse.get_pressed()[0]:
            bool_value_error = False

    if int_check_starter == 1:
        int_time_start = time.perf_counter()
        int_check_starter += 1

    if time.perf_counter() - int_time_start >= 5.0:
        bool_value_error = False


def morse_setting():
    global bool_morse_setting_clicked, temp_text_dot, temp_text_, bool_check_text_box_dot, bool_check_text_box_, mouse_pos
    surface_screen_morse_setting = pygame.Surface((750, 600)).convert_alpha()
    surface_screen_morse_setting.fill((118, 118, 118))
    surface_screen_morse_setting.set_alpha(230)
    surface_screen.blit(surface_screen_morse_setting, (175, 0))

    # Thoát cửa sổ
    pos_morse_setting = (175, 0)
    rect_morse_setting = pygame.rect.Rect(pos_morse_setting + surface_screen_morse_setting.get_size())
    rect_button_setting = pygame.rect.Rect(surface_button_setting.rect)

    if not rect_morse_setting.collidepoint(mouse_pos) and not rect_button_setting.collidepoint(mouse_pos):
        if pygame.mouse.get_pressed()[0]:
            bool_morse_setting_clicked = False

    # Hiển thị chữ
    surface_screen.blit(text_Setting, (466, 25))
    surface_screen.blit(text_Characters, (200, 100))
    surface_screen.blit(text_Volume, (200, 200))

    # Đổi kí tự
    text_box_dot.update(events)

    if text_box_dot.get_text() == text_box_.get_text():
        text_box_.set_text("")

    if text_box_dot.get_check_press():
        temp_text_dot = text_box_dot.get_text()
        if not bool_check_text_box_dot:
            bool_check_text_box_dot = True
            text_box_dot.clear_text()
    elif not text_box_dot.get_check_press():
        bool_check_text_box_dot = False
        text_box_dot.set_text(temp_text_dot)

    if not text_box_dot.get_check_press():
        text_box_dot.set_text(temp_text_dot)
    if len(text_box_dot.get_text()) > 1:
        text_box_dot.set_text(text_box_dot.get_text()[:-1])
    text_box_dot.cursor_visible = False
    text_box_dot.render(surface_screen)
    text_box_dot.set_text_note("...")

    surface_screen.blit(text_to_dot, (400, 105))

    text_box_.update(events)

    if text_box_.get_text() == text_box_dot.get_text():
        text_box_.set_text("")

    if text_box_.get_check_press():
        temp_text_ = text_box_.get_text()
        if not bool_check_text_box_:
            bool_check_text_box_ = True
            text_box_.clear_text()
    elif not text_box_.get_check_press():
        bool_check_text_box_ = False
        text_box_.set_text(temp_text_)

    if not text_box_.get_check_press():
        text_box_.set_text(temp_text_)
    if len(text_box_.get_text()) > 1:
        text_box_.set_text(text_box_.get_text()[:-1])
    text_box_.cursor_visible = False
    text_box_.render(surface_screen)
    text_box_.set_text_note("...")

    surface_screen.blit(text_to_, (400, 150))

    # Thanh kéo âm thanh
    slider_morse_sound_setting_event()
    pygame_widgets.update(events)


def play_morse_code(morse_code, volume=1.0, dot_duration=0.1, frequency=440):
    dash_duration = 3 * dot_duration
    pause_duration = dot_duration
    space_duration = 7 * dot_duration

    dot_waveform = np.sin(2 * np.pi * frequency * np.arange(int(dot_duration * 44100)) / 44100)
    dash_waveform = np.sin(2 * np.pi * frequency * np.arange(int(dash_duration * 44100)) / 44100)
    pause_waveform = np.zeros(int(pause_duration * 44100))
    space_waveform = np.zeros(int(space_duration * 44100))

    waveform = []
    for char in morse_code:
        if char == ".":
            waveform.append(dot_waveform)
        elif char == "-":
            waveform.append(dash_waveform)
        elif char == " ":
            waveform.append(space_waveform)
        elif char == "\n":
            waveform.append(space_waveform)
        else:
            continue

        waveform.append(pause_waveform)

    try:
        waveform = np.concatenate(waveform)
        waveform *= volume

        sounddevice.play(waveform, samplerate=44100)
    except Exception:
        ...


# Hàm chế độ SEMAPHORE
def SEMAPHORE():
    global bool_semaphore_clicked, bool_opencv_screen_clicked, bool_video_active, fps, cap, int_width_cap, int_height_cap

    clock.tick(fps)

    surface_screen.fill((25, 25, 25))
    pygame.draw.rect(surface_screen, (255, 255, 255), (175, 100, 750, 400), 1)

    surface_screen.blit(text_SEMAPHORE, (363, 20))
    surface_screen.blit(image_leaf, (900, 340))

    if surface_button_live.draw(surface_screen):
        effect_clicked()
        bool_semaphore_clicked = False
        bool_opencv_screen_clicked = True
        bool_video_active = True
        cap = cv2.VideoCapture(1)

        input_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        input_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        int_width_cap = int(input_width * min(750 / input_width, 500 / input_height))
        int_height_cap = int(input_height * min(750 / input_width, 500 / input_height))

    if surface_button_import_file.draw(surface_screen):
        effect_clicked()
        filename = askopenfilename()
        if filename != "":
            bool_semaphore_clicked = False
            bool_opencv_screen_clicked = True
            bool_video_active = True
            cap = cv2.VideoCapture(filename)

            input_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            input_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

            int_width_cap = int(input_width * min(750 / input_width, 500 / input_height))
            int_height_cap = int(input_height * min(750 / input_width, 500 / input_height))

    if surface_back_button.draw(surface_screen):
        effect_clicked()
        bool_semaphore_clicked = False


def get_angle(a, b, c):
    angle = degrees(atan2(c["y"] - b["y"], c["x"] - b["x"]) - atan2(a["y"] - b["y"], a["x"] - b["x"]))
    return angle + 360 if angle < 0 else angle


def get_limb_direction(p1, p2, p3, closest_degrees=45):
    closest_angle = angle = get_angle(p1, p2, p3)

    mod_close = angle % closest_degrees
    if mod_close < closest_degrees / 2:
        closest_angle -= mod_close
    else:
        closest_angle += closest_degrees - mod_close

    closest_angle = int(closest_angle)

    if closest_angle > 180:
        closest_angle = closest_angle - 360
    if angle > 180:
        angle = angle - 360

    if closest_angle == 0 and angle < -30:
        closest_angle -= 45
    elif closest_angle == -90 and angle > -80:
        closest_angle += 45
    elif closest_angle == -90 and angle < -110:
        closest_angle -= 45

    elif closest_angle == 0 and angle > 30:
        closest_angle += 45
    elif closest_angle == 90 and angle < 80:
        closest_angle -= 45
    elif closest_angle == 90 and angle > 110:
        closest_angle += 45

    elif closest_angle == 180:
        if 0 > angle > -167:
            closest_angle = -135
        elif 0 < angle < 167:
            closest_angle = 135

    return closest_angle

def type_semaphore(armL_angle, armR_angle, numerals=False, allow_repeat=None):
    global current_semaphore, SEMAPHORES

    arm_match = SEMAPHORES.get((armR_angle, armL_angle), "") or SEMAPHORES.get((armL_angle, armR_angle), "")
    if arm_match:
        current_semaphore = arm_match.get("n", "") if numerals else arm_match.get("a", "")
        type_and_remember(allow_repeat)
        return current_semaphore

    return False

def type_and_remember(allow_repeat=False):
    global current_semaphore, last_keys

    if len(current_semaphore) == 0:
        return
    keys = [current_semaphore]
    if allow_repeat or (keys != last_keys):
        last_keys = keys.copy()
        current_semaphore = ""

def get_key_text(keys):
    return keys[-1] if keys else ""

def output(keys, image):
    keystring = "+".join(keys)
    if keystring:
        to_display = "space" if get_key_text(keys) == " " else "numeral" if get_key_text(keys) == "N" else "delete" if get_key_text(keys) == "D" else get_key_text(keys)
        text_size, _ = cv2.getTextSize(to_display, cv2.FONT_HERSHEY_SIMPLEX, 5, 10)

        input_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        input_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        frame_midpoint = (int((input_width - text_size[0]) / 2), int((input_height + text_size[1]) / 2))

        cv2.putText(image, to_display, frame_midpoint, cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 255), 10)


def OpenCV_screen():
    global bool_opencv_screen_clicked, bool_semaphore_clicked, bool_video_active, fps, cap, last_frames, last_keys, NUMERAL, counter, int_width_cap, int_height_cap

    clock.tick(fps)

    surface_screen.fill((25, 25, 25))
    pygame.draw.rect(surface_screen, (255, 255, 255), ((1100 - int_width_cap - 2) / 2, (600 - int_height_cap - 2) / 2, int_width_cap + 2, int_height_cap + 2), 1)

    if surface_back_button.draw(surface_screen):
        effect_clicked()

        bool_opencv_screen_clicked = False
        bool_video_active = False
        bool_semaphore_clicked = True

    FLIP = False

    if bool_video_active:
        success, image = cap.read()
        if not success:
            bool_video_active = False

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pose_results = pose_model.process(image)

        # draw pose
        mp.solutions.drawing_utils.draw_landmarks(
            image,
            pose_results.pose_landmarks,
            mp.solutions.pose.POSE_CONNECTIONS,
            DEFAULT_LANDMARKS_STYLE)

        if FLIP:
            image = cv2.flip(image, 1)

        if pose_results.pose_landmarks:
            last_frames = last_frames[1:] + [empty_frame.copy()]

            body = []
            for point in pose_results.pose_landmarks.landmark:
                body.append({
                    "x": 1 - point.x,
                    "y": 1 - point.y,
                    "visibility": point.visibility
                })

            elbowL, shoulderL, hipL = body[15], body[11], body[23]
            armL = (elbowL, shoulderL, hipL)

            elbowR, shoulderR, hipR = body[16], body[12], body[24]
            armR = (elbowR, shoulderR, hipR)

            armL_angle = get_limb_direction(*armL)
            armR_angle = get_limb_direction(*armR)

            if type_semaphore(armL_angle, armR_angle, NUMERAL):
                last_frames[-1]["signed"] = True

                if get_key_text(last_keys) == "N":
                    counter += 1

                if counter >= 2 and get_key_text(last_keys) == "N":
                    NUMERAL = not NUMERAL
                    counter = 0

                output(get_key_text(last_keys), image)

        image = cv2.resize(image, (int_width_cap, int_height_cap))
        image = cv2.flip(np.rot90(image), 0)
        image = pygame.surfarray.make_surface(image)
        surface_screen.blit(image, ((1100 - int_width_cap) / 2, (600 - int_height_cap) / 2))
    else:
        cv2.destroyAllWindows()


# Hàm chế độ cài đặt
def options():
    global fps, bool_options_clicked, bool_check_FPS, bool_check_music, bool_check_effect, text_options, image_scale, image_fps, text_fps, image_music, text_music, image_effect, text_effect, temp_val_music, temp_val_effect, bool_status_mod, temp_val_morse_sound_setting

    int_dt = clock.tick(fps) / 1000.0

    surface_screen.fill((25, 25, 25))

    # Text Options
    surface_screen.blit(text_options, (438.5, 40))

    # FPS
    surface_screen.blit(image_fps, (200, 150))
    surface_screen.blit(text_fps, (300, 165))

    # MUSIC
    surface_screen.blit(image_music, (200, 300))
    surface_screen.blit(text_music, (300, 315))

    # EFFECT
    surface_screen.blit(image_effect, (200, 450))
    surface_screen.blit(text_effect, (300, 465))

    # Xử lí điều kiện chỉnh âm lượng
    slider_music_event()
    slider_effect_event()

    pygame_widgets.update(events)

    try:
        pygame.mixer.music.set_volume(slider_music.getValue() / 100)
        sound_click_sfx.set_volume(slider_effect.getValue() / 100)
    except Exception:
        ...

    # Xử lí điều kiện
    if surface_button_animation_options_fps.draw(surface_screen, int_dt):
        effect_clicked()
        bool_check_FPS = not bool_check_FPS

    if surface_button_animation_options_music.draw(surface_screen, int_dt):
        effect_clicked()
        bool_check_music = not bool_check_music
        if bool_check_music:
            try:
                pygame.mixer.music.unpause()
            except Exception:
                ...
        else:
            try:
                pygame.mixer.music.pause()
            except Exception:
                ...

        if not bool_check_music:
            temp_val_music = slider_music.getValue()
            slider_music.setValue(0)
        else:
            try:
                slider_music.setValue(temp_val_music)
            except ValueError:
                pass

    if surface_button_animation_options_effect.draw(surface_screen, int_dt):
        bool_check_effect = not bool_check_effect

        effect_clicked()
        if not bool_check_effect:
            temp_val_effect = slider_effect.getValue()
            slider_effect.setValue(0)
        else:
            try:
                slider_effect.setValue(temp_val_effect)
            except ValueError:
                pass

    if surface_button_reset.draw(surface_screen):
        effect_clicked()
        if not bool_check_FPS == bool(read_json("options_default.json")["options"]["bool_check_FPS"]):
            surface_button_animation_options_fps.active()
        if not bool_check_music == bool(read_json("options_default.json")["options"]["bool_check_music"]):
            surface_button_animation_options_music.active()
        if not bool_check_effect == bool(read_json("options_default.json")["options"]["bool_check_effect"]):
            surface_button_animation_options_effect.active()
        if not bool_status_mod == bool(read_json("options_default.json")["morse_settings"]["bool_status_mod"]):
            change_mod()
        temp_val_music = int(read_json("options_default.json")["options"]["temp_val_music"])
        slider_music.setValue(int(temp_val_music))
        temp_val_effect = int(read_json("options_default.json")["options"]["temp_val_effect"])
        slider_effect.setValue(int(temp_val_music))
        temp_val_morse_sound_setting = int(
            read_json("options_default.json")["morse_settings"]["temp_val_morse_sound_setting"])
        slider_morse_sound_setting.setValue(int(temp_val_morse_sound_setting))

    if surface_back_button.draw(surface_screen):
        effect_clicked()
        bool_options_clicked = False


def read_json(filename):
    file = open(filename, "r", encoding="utf-8")
    data = json.loads(file.read())
    file.close()
    return data


def save_json():
    file = open("options.json", "w", encoding="utf-8")
    dictionary = {"options": {}, "morse_settings": {}}

    dictionary["options"]["bool_check_FPS"] = str(bool_check_FPS).replace("False", "")
    dictionary["options"]["bool_check_music"] = str(bool_check_music).replace("False", "")
    dictionary["options"]["bool_check_effect"] = str(bool_check_effect).replace("False", "")
    dictionary["morse_settings"]["bool_status_mod"] = str(bool_status_mod).replace("False", "")
    dictionary["options"]["temp_val_music"] = slider_music.getValue()
    dictionary["options"]["temp_val_effect"] = slider_effect.getValue()
    dictionary["morse_settings"]["temp_val_morse_sound_setting"] = slider_morse_sound_setting.getValue()

    file.write(json.dumps(dictionary, indent=4, ensure_ascii=False))
    file.close()


def load_data():
    global bool_load, temp_val_music, temp_val_effect, temp_val_morse_sound_setting
    # Load dữ liệu
    if not bool_load:
        slider_music.setValue(temp_val_music)
        slider_effect.setValue(temp_val_effect)
        slider_morse_sound_setting.setValue(temp_val_morse_sound_setting)
        bool_load = True

    try:
        pygame.mixer.music.set_volume(slider_music.getValue() / 100)
        sound_click_sfx.set_volume(slider_effect.getValue() / 100)
    except Exception:
        ...


def slider_morse_sound_setting_event():
    global temp_val_morse_sound_setting
    slider_morse_sound_setting.show()
    slider_morse_sound_setting.enable()

    output_morse_sound_setting.clear_text_check(True)

    load_data()

    if output_morse_sound_setting.get_check_press():
        if output_morse_sound_setting.get_text() != "":
            try:
                slider_morse_sound_setting.setValue(int(output_morse_sound_setting.get_text()))
                if slider_morse_sound_setting.getValue() > 100:
                    slider_morse_sound_setting.setValue(100)
                    output_morse_sound_setting.set_text(str(slider_morse_sound_setting.getValue()))
                    temp_val_morse_sound_setting = slider_morse_sound_setting.getValue()
                if len(output_morse_sound_setting.get_text()) > 3:
                    slider_morse_sound_setting.setValue(temp_val_morse_sound_setting)
                    output_morse_sound_setting.set_text(str(slider_morse_sound_setting.getValue()))
            except ValueError:
                if len(output_morse_sound_setting.get_text()) > 3:
                    slider_morse_sound_setting.setValue(temp_val_morse_sound_setting)
                    output_morse_sound_setting.set_text(str(slider_morse_sound_setting.getValue()))

    else:
        output_morse_sound_setting.set_text(str(slider_morse_sound_setting.getValue()))

    output_morse_sound_setting.render(surface_screen, (68, 68, 68), 0.8)
    output_morse_sound_setting.update(events)


def slider_music_event():
    global temp_val_music
    slider_music.show()
    slider_music.enable()

    output_music.clear_text_check(True)

    if output_music.get_check_press():
        if output_music.get_text() != "":
            try:
                slider_music.setValue(int(output_music.get_text()))
                if slider_music.getValue() > 100:
                    slider_music.setValue(100)
                    output_music.set_text(str(slider_music.getValue()))
                    temp_val_music = slider_music.getValue()
                if len(output_music.get_text()) > 3:
                    slider_music.setValue(temp_val_music)
                    output_music.set_text(str(slider_music.getValue()))
            except ValueError:
                if len(output_music.get_text()) > 3:
                    slider_music.setValue(temp_val_music)
                    output_music.set_text(str(slider_music.getValue()))

    else:
        output_music.set_text(str(slider_music.getValue()))

    if not bool_check_music:
        slider_music.setValue(0)

    output_music.render(surface_screen, (68, 68, 68), 0.8)
    output_music.update(events)


def slider_effect_event():
    global temp_val_effect
    slider_effect.show()
    slider_effect.enable()

    output_effect.clear_text_check(True)

    if output_effect.get_check_press():
        if output_effect.get_text() != "":
            try:
                slider_effect.setValue(int(output_effect.get_text()))
                if slider_effect.getValue() > 100:
                    slider_effect.setValue(100)
                    output_effect.set_text(str(slider_effect.getValue()))
                    temp_val_effect = slider_effect.getValue()
                if len(output_effect.get_text()) > 3:
                    slider_effect.setValue(temp_val_effect)
                    output_effect.set_text(str(slider_effect.getValue()))
            except ValueError:
                if len(output_effect.get_text()) > 3:
                    slider_effect.setValue(temp_val_effect)
                    output_effect.set_text(str(slider_effect.getValue()))

    else:
        output_effect.set_text(str(slider_effect.getValue()))

    if not bool_check_effect:
        slider_effect.setValue(0)

    output_effect.render(surface_screen, (68, 68, 68), 0.8)
    output_effect.update(events)


# MENU
def menu():
    global bool_running, bool_options_clicked, bool_morse_clicked, bool_semaphore_clicked, bool_help_clicked, fps

    # Giới hạn FPS
    clock.tick(fps)

    # Đổi màu nền
    surface_screen.fill((25, 25, 25))

    # Chữ
    surface_screen.blit(text_code_translation, (340, 100))

    # Chế độ MORSE
    if surface_button_morse.draw(surface_screen):
        effect_clicked()
        bool_morse_clicked = True

    # Chế độ SEMAPHORE
    if surface_button_semaphore.draw(surface_screen):
        effect_clicked()
        bool_semaphore_clicked = True

    # Chế độ thoát
    if surface_button_quit.draw(surface_screen):
        effect_clicked()
        bool_running = False

    # Chế độ cài đặt
    if surface_button_options.draw(surface_screen):
        effect_clicked()
        bool_options_clicked = True


# Chương trình chính
bool_running = True
bool_check_FPS = bool(read_json("options.json")["options"]["bool_check_FPS"])
bool_check_music = bool(read_json("options.json")["options"]["bool_check_music"])
bool_check_effect = bool(read_json("options.json")["options"]["bool_check_effect"])
bool_options_clicked = False
bool_morse_clicked = False
bool_semaphore_clicked = False
bool_morse_setting_clicked = False
bool_opencv_screen_clicked = False
bool_video_active = False
bool_help_clicked = False
bool_value_error = False
bool_status_mod = bool(read_json("options.json")["morse_settings"]["bool_status_mod"])
bool_help_menu = True
bool_help_morse = False
bool_help_semaphore = False
bool_help_options = False
bool_load = False
bool_check_text_box_dot = False
bool_check_text_box_ = False

events = pygame.event.get()
mouse_pos = pygame.mouse.get_pos()

clock = pygame.time.Clock()
fps = 60

try:
    if not bool_check_music:
        pygame.mixer.music.pause()
except Exception:
    ...

# Semaphore
int_width_cap = 0
int_height_cap = 0

cap = cv2.VideoCapture(0)

pose_model = mp.solutions.pose.Pose()

DEFAULT_LANDMARKS_STYLE = mp.solutions.drawing_styles.get_default_pose_landmarks_style()
DEFAULT_HAND_CONNECTIONS_STYLE = mp.solutions.drawing_styles.get_default_hand_connections_style()

FPS = 24

VISIBILITY_THRESHOLD = .8
STRAIGHT_LIMB_MARGIN = 20
EXTENDED_LIMB_MARGIN = .8

SEMAPHORES = {
            (0, 0): {"a": " ", "n": " "},
            (-45, 0): {"a": "a", "n": "1"},
            (-90, 0): {"a": "b", "n": "2"},
            (-135, 0): {"a": "c", "n": "3"},
            (180, 0): {"a": "d", "n": "4"},
            (0, 135): {"a": "e", "n": "5"},
            (0, 90): {"a": "f", "n": "6"},
            (0, 45): {"a": "g", "n": "7"},
            (-90, -45): {"a": "h", "n": "8"},
            (-135, -45): {"a": "i", "n": "9"},
            (180, 90): {"a": "j", "n": "0"},
            (-45, 180): {"a": "k"},
            (-45, 135): {"a": "l"},
            (-45, 90): {"a": "m"},
            (-45, 45): {"a": "n"},
            (-135, -90): {"a": "o"},
            (-90, 180): {"a": "p"},
            (-90, 135): {"a": "q"},
            (-90, 90): {"a": "r"},
            (-90, 45): {"a": "s"},
            (180, -135): {"a": "t"},
            (-135, 135): {"a": "u"},
            (180, 45): {"a": "v"},
            (135, 90): {"a": "w"},
            (45, 135): {"a": "x"},
            (-135, 90): {"a": "y"},
            (45, 90): {"a": "z"},
            (135, 180): {"a": "N", "n": "N"},
            (-135, 45): {"a": "D", "n": "D"},
        }

FRAME_HISTORY = 5

empty_frame = {
    "signed": False,
}
last_frames = FRAME_HISTORY * [empty_frame.copy()]

frame_midpoint = (0, 0)

current_semaphore = ""
last_keys = []
counter = 0
NUMERAL = False

# Bộ nhớ
temp_val_music = read_json("options.json")["options"]["temp_val_music"]
temp_val_effect = read_json("options.json")["options"]["temp_val_effect"]
temp_val_morse_sound_setting = int(read_json("options.json")["morse_settings"]["temp_val_morse_sound_setting"])
temp_pos1 = 630
temp_pos2 = 80
temp_text_dot = ""
temp_text_ = ""
text_temp1 = ""
text_temp2 = ""
int_check_starter = 0
int_time_start = 0
string_input = ""

# Morse
dic_morse_to_text = {'.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F', '--.': 'G', '....': 'H',
                     '..': 'I',
                     '.---': 'J', '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P', '--.-': 'Q',
                     '.-.': 'R',
                     '...': 'S', '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y', '--..': 'Z',
                     '.----': '1', '..---': '2', '...--': '3', '....-': '4', '.....': '5', '-....': '6', '--...': '7',
                     '---..': '8', '----.': '9', '-----': '0', '/': ' '}
dic_text_to_morse = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
                     'I': '..',
                     'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-',
                     'R': '.-.',
                     'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..',
                     '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
                     '8': '---..', '9': '----.', '0': '-----', ' ': '/'}

# Ảnh
image_scale = 0.15

image_fps = pygame.image.load("asset\\Image\\FPS.png").convert_alpha()
image_fps_size = image_fps.get_size()
image_fps = pygame.transform.smoothscale(image_fps, (image_fps_size[0] * image_scale, image_fps_size[1] * image_scale))

image_music = pygame.image.load("asset\\Image\\MUSIC.png").convert_alpha()
image_music_size = image_music.get_size()
image_music = pygame.transform.smoothscale(image_music,
                                           (image_music_size[0] * image_scale, image_music_size[1] * image_scale))

image_effect = pygame.image.load("asset\\Image\\EFFECT.png").convert_alpha()
image_effect_size = image_effect.get_size()
image_effect = pygame.transform.smoothscale(image_effect,
                                            (image_effect_size[0] * image_scale, image_effect_size[1] * image_scale))

image_quit = pygame.image.load("asset\\Image\\QUIT.png").convert_alpha()

image_options = pygame.image.load("asset\\Image\\OPTIONS.png").convert_alpha()

image_back_button = pygame.image.load("asset\\Image\\BACK.png").convert_alpha()

image_change = pygame.image.load("asset\\Image\\CHANGE.png").convert_alpha()

image_copy = pygame.image.load("asset\\Image\\COPY.png").convert_alpha()

image_setting = pygame.image.load("asset\\Image\\SETTING.png").convert_alpha()

image_speaker = pygame.image.load("asset\\Image\\SPEAKER.png").convert_alpha()

image_upload = pygame.image.load("asset\\Image\\UPLOAD.png").convert_alpha()

image_leaf = pygame.image.load("asset\\Image\\LEAF.png").convert_alpha()
image_leaf_size = image_leaf.get_size()
image_leaf = pygame.transform.smoothscale(image_leaf,
                                          (image_leaf_size[0] * 0.5, image_leaf_size[1] * 0.5))

image_warning = pygame.image.load("asset\\Image\\WARNING.png").convert_alpha()
image_warning_size = image_warning.get_size()
image_warning = pygame.transform.smoothscale(image_warning,
                                             (image_warning_size[0] * 0.25, image_warning_size[1] * 0.25))

# Các chữ
text_options = pygame.font.Font("asset\\Font\\Montserrat-Regular.ttf", 56).render("Options", True, "#FFFFFF")

text_fps = pygame.font.Font("asset\\Font\\Public-Sans-Thin.ttf", 33).render("Frames - per second", True, "#FFFFFF")

text_music = pygame.font.Font("asset\\Font\\Public-Sans-Thin.ttf", 33).render("Music", True, "#FFFFFF")

text_effect = pygame.font.Font("asset\\Font\\Public-Sans-Thin.ttf", 33).render("Effect", True, "#FFFFFF")

text_code_translation = pygame.font.Font("asset\\Font\\SIFONN_BASIC_OUTLINE.otf", 66).render("CODE TRANSLATION",
                                                                                             True, "#FFFFFF")

text_MORSE_title = pygame.font.Font("asset\\Font\\Saira-Thin.ttf", 60).render("MORSE", True, "#FFFFFF")

text_Document = pygame.font.Font("asset\\Font\\Public-Sans-Thin.ttf", 30).render("Document", True, '#FFFFFF')

text_Morse = pygame.font.Font("asset\\Font\\Public-Sans-Thin.ttf", 30).render("Morse", True, '#FFFFFF')

text_Setting = pygame.font.Font("asset\\Font\\Public-Sans-Thin.ttf", 50).render("Setting", True, "#FFFFFF")

text_Characters = pygame.font.Font("asset\\Font\\Montserrat-Regular.ttf", 30).render("Charaters:", True, "#FFFFFF")

text_to_ = pygame.font.Font("asset\\Font\\Montserrat-Regular.ttf", 26).render("to _", True, "#FFFFFF")
text_to_dot = pygame.font.Font("asset\\Font\\Montserrat-Regular.ttf", 26).render("to .", True, "#FFFFFF")

text_Volume = pygame.font.Font("asset\\Font\\Montserrat-Regular.ttf", 30).render("Volume:", True, "#FFFFFF")

text_SEMAPHORE = pygame.font.Font("asset\\Font\\Saira-Thin.ttf", 60).render("SEMAPHORE", True, "#FFFFFF")

text_COMING_SOON = pygame.font.Font("asset\\Font\\Saira-Thin.ttf", 120).render("COMING SOON!", True, "#FFFFFF")

text_box = TextInputBox(30,
                        200,
                        510,
                        300,
                        10,
                        10,
                        font_family="asset\\Font\\Rokkitt-Thin.ttf",
                        font_size=26
                        )

text_box2 = TextInputBox(560,
                         200,
                         510,
                         300,
                         10,
                         10,
                         font_family="asset\\Font\\Rokkitt-Thin.ttf",
                         font_size=26,
                         status=False
                         )

text_box_dot = TextInputBox(370,
                            105,
                            35,
                            35,
                            font_family="asset\\Font\\Montserrat-Regular.ttf",
                            font_size=26
                            )

text_box_ = TextInputBox(370,
                         150,
                         35,
                         35,
                         font_family="asset\\Font\\Montserrat-Regular.ttf",
                         font_size=26
                         )

text_Document_surface = surface_screen.blit(text_Document, (temp_pos1, 150))

text_Morse_surface = surface_screen.blit(text_Morse, (temp_pos2, 150))

text_value_error = pygame.font.Font("asset\\Font\\Montserrat-Regular.ttf",
                                    50).render("File format have to .txt",
                                               True,
                                               "#000000")

if bool_status_mod:
    change_mod()

# Kiểu chữ
font_fps = pygame.font.Font(None, 30)

# Các nút
surface_button_morse = Button_TEXT("MORSE",
                                   ("asset\\Font\\SIFONN_BASIC_OUTLINE.otf", 42),
                                   412,
                                   144,
                                   (100, 210),
                                   (41, 41, 41),
                                   20)
surface_button_morse.border((68, 68, 68), 10)

surface_button_semaphore = Button_TEXT("SEMAPHORE",
                                       ("asset\\Font\\SIFONN_BASIC_OUTLINE.otf", 40),
                                       412,
                                       144,
                                       (588, 210),
                                       (41, 41, 41),
                                       20)
surface_button_semaphore.border((68, 68, 68), 10)

surface_button_live = Button_TEXT("LIVE",
                                  ("asset\\Font\\SIFONN_BASIC_OUTLINE.otf", 42),
                                  412,
                                  144,
                                  (100, 210),
                                  (41, 41, 41),
                                  20)
surface_button_live.border((68, 68, 68), 10)

surface_button_import_file = Button_TEXT("IMPORT FILE",
                                         ("asset\\Font\\SIFONN_BASIC_OUTLINE.otf", 40),
                                         412,
                                         144,
                                         (588, 210),
                                         (41, 41, 41),
                                         20)
surface_button_import_file.border((68, 68, 68), 10)

surface_button_help = Button_TEXT("HELP",
                                  ("asset\\Font\\FontsFree-Net-Montserrat-ExtraLight.ttf", 20),
                                  100,
                                  50,
                                  (950, 525),
                                  (41, 41, 41),
                                  10)
surface_button_help.border((68, 68, 68), 10)

surface_button_reset = Button_TEXT("RESET",
                                   ("asset\\Font\\FontsFree-Net-Montserrat-ExtraLight.ttf", 20),
                                   100,
                                   50,
                                   (50, 525),
                                   (41, 41, 41),
                                   10)
surface_button_reset.border((68, 68, 68), 10)

surface_button_quit = Button_IMG(1070, 30, image_quit, 0.1, 0.02)

surface_button_quit_help = Button_IMG(970, 80, image_quit, 0.1, 0.02)

surface_button_options = Button_IMG(30, 30, image_options, 0.1, 0.02)

surface_back_button = Button_IMG(80, 31, image_back_button, 0.2, 0.02)

surface_button_animation_options_fps = Animation_Toggle((900, 165),
                                                        100,
                                                        50,
                                                        30,
                                                        bool_check_FPS)
surface_button_animation_options_fps.set_circle_color((25, 25, 25))
surface_button_animation_options_fps.set_speed(300)

surface_button_animation_options_music = Animation_Toggle((900, 315),
                                                          100,
                                                          50,
                                                          30,
                                                          bool_check_music)
surface_button_animation_options_music.set_circle_color((25, 25, 25))
surface_button_animation_options_music.set_speed(300)

surface_button_animation_options_effect = Animation_Toggle((900, 465), 100, 50, 30, bool_check_effect)
surface_button_animation_options_effect.set_circle_color((25, 25, 25))
surface_button_animation_options_effect.set_speed(300)

surface_button_change = Button_IMG(550, 180, image_change, 0.05, 0.01)

surface_button_copy = Button_IMG(1055, 520, image_copy, 0.06, 0.01)

surface_button_speaker = Button_IMG(1022, 520, image_speaker, 0.06, 0.01)

surface_button_setting = Button_IMG(1060, 40, image_setting, 0.1, 0.02)

surface_button_upload = Button_IMG(989, 520, image_upload, 0.06, 0.01)

# Thanh kéo
slider_music = Slider(surface_screen,
                      450,
                      330,
                      250,
                      20,
                      min=0,
                      max=100,
                      step=1,
                      handleColour=(255, 255, 255))
slider_music.hide()
slider_music.disable()

output_music = TextInputBox(750,
                            320,
                            60,
                            40,
                            10,
                            8,
                            text_color=(255, 255, 255),
                            font_size=20,
                            align_text="center",
                            font_family="asset\\Font\\Public-Sans-Thin.ttf")
output_music.set_text("50")

slider_effect = Slider(surface_screen,
                       450,
                       480,
                       250,
                       20,
                       min=0,
                       max=100,
                       step=1,
                       handleColour=(255, 255, 255))
slider_effect.hide()
slider_effect.disable()

output_effect = TextInputBox(750,
                             470,
                             60,
                             40,
                             10,
                             8,
                             text_color=(255, 255, 255),
                             font_size=20,
                             align_text="center",
                             font_family="asset\\Font\\Public-Sans-Thin.ttf")
output_effect.set_text("50")

slider_morse_sound_setting = Slider(surface_screen, 350, 210, 250, 20, min=0, max=100, step=1)
slider_morse_sound_setting.hide()
slider_morse_sound_setting.disable()

output_morse_sound_setting = TextInputBox(620,
                                          200,
                                          60,
                                          40,
                                          10,
                                          8,
                                          text_color=(255, 255, 255),
                                          font_size=20,
                                          align_text="center",
                                          font_family="asset\\Font\\Public-Sans-Thin.ttf")
output_morse_sound_setting.set_text("50")

# Âm thanh
try:
    pygame.mixer.init()
    pygame.mixer.music.load("asset\\Sound\\music.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_endevent(pygame.USEREVENT)
    pygame.mixer_music.set_volume(0.5)
    if not bool_check_music:
        pygame.mixer.music.pause()

    sound_click_sfx = pygame.mixer.Sound("asset\\Sound\\Click.wav")

except Exception:
    ...

load_data()


def main():
    global bool_running, events, mouse_pos
    while bool_running:
        # Sự kiện trong chương trình
        mouse_pos = pygame.mouse.get_pos()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                bool_running = False
            elif event.type == pygame.USEREVENT and bool_check_music:
                try:
                    pygame.mixer.music.play()
                except Exception:
                    ...

        if bool_options_clicked:
            options()
            if bool_help_clicked:
                help_options()
        elif bool_morse_clicked:
            MORSE()
            if bool_help_clicked:
                help_MORSE()
        elif bool_semaphore_clicked:
            SEMAPHORE()
            if bool_help_clicked:
                help_SEMAPHORE()
        elif bool_opencv_screen_clicked:
            OpenCV_screen()
        else:
            menu()
            slider_music.hide()
            slider_music.disable()
            slider_effect.hide()
            slider_effect.disable()
            slider_morse_sound_setting.hide()
            slider_morse_sound_setting.disable()
            if bool_help_clicked:
                help_menu()
                surface_button_morse.disable()
                surface_button_semaphore.disable()
                surface_button_options.disable()
            else:
                surface_button_morse.enable()
                surface_button_semaphore.enable()
                surface_button_options.enable()

        if bool_check_FPS:
            fps_screen = font_fps.render("FPS {}".format(int(clock.get_fps())), True, (255, 255, 255))
            rect_fps = pygame.rect.Rect(0, 580, fps_screen.get_width(), fps_screen.get_height())
            if rect_fps.collidepoint(mouse_pos):
                fps_screen = font_fps.render("MAX FPS: {}".format(fps), True, (255, 255, 255))
            surface_screen.blit(fps_screen, (0, 580))

        pygame.display.flip()

    save_json()
    pygame.quit()


if __name__ == "__main__":
    main()
