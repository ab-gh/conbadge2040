import badger2040
import qrcode

badger2040.system_speed(0) # lets save some battery

display = badger2040.Badger2040()

display.update_speed(2)

code = qrcode.QRCode()

def measure_qr_code(size, code):
    w, h = code.get_size()
    module_size = int(size / w)
    return module_size * w, module_size


def draw_qr_code(ox, oy, size, code):
    size, module_size = measure_qr_code(size, code)
    display.pen(15)
    display.rectangle(ox, oy, size, size)
    display.pen(0)
    for x in range(size):
        for y in range(size):
            if code.get_module(x, y):
                display.rectangle(ox + x * module_size, oy + y * module_size, module_size, module_size)


# Name Badge Mode
def mode1(qr):
    display.pen(15)
    display.clear()
    # Hello top banner
    display.pen(0)
    display.rectangle(0, 0, 298, 40)
    display.thickness(4)
    display.font("sans")
    display.pen(15)
    display.text("Kepler!", 86, 18, scale=1.2)
    
    if qr:
        qr = bytearray(int(96 * 96 / 8))
        open("qr.bin", "r").readinto(qr)
        display.icon(qr, 0, 96, 96, 198, 40)
    else:
        kep = bytearray(int(96 * 96 / 8))
        open("badge.bin", "r").readinto(kep)
        display.icon(kep, 0, 96, 96, 198, 40)
    
    # Text
    display.thickness(2)
    display.pen(0)
    display.text("Web: kep.dog",8, 60, scale=0.8)
    display.text("Tele: @kepwoof",8, 85, scale=0.8)
    display.text("Twit: @kepwoof",8, 110, scale=0.8)
    
    # Button Icons
    display.pen(0)
    display.rectangle(38+3, 122+3, 5, 3)
    display.pen(15)
    display.pixel(41+3, 123+3)
    
    display.pen(0)
    display.rectangle(148, 122+3, 4, 4)
    display.pen(15)
    display.rectangle(148, 122+5, 2, 2)
    display.rectangle(148+2, 122, 4, 4)


# Photography Mode
def mode2(qr, photos):
    display.pen(15)
    display.clear()
    
    # Hello top banner
    display.pen(0)
    display.rectangle(0, 0, 298, 40)
    display.thickness(3)
    display.font("sans")
    display.pen(15)
    display.text("Kepwoof Photography", 13, 18, scale=0.8)
    
    if qr:
        qr = bytearray(int(96 * 96 / 8))
        open("photoqr.bin", "r").readinto(qr)
        display.icon(qr, 0, 96, 96, 198, 40)
    else:
        kep = bytearray(int(96 * 96 / 8))
        open("photo.bin", "r").readinto(kep)
        display.icon(kep, 0, 96, 96, 198, 40)
    display.thickness(2)
    display.pen(0)
    display.text("Free photos!", 8, 60, scale=0.8)
    display.text("photos.kep.dog", 8, 85, scale=0.8)
    display.text("Pic Count: ", 8, 110, scale=0.8)
    display.font("bitmap6")
    display.text(str(photos), 140, 100, scale=3)
    
    # Button Icons
    display.pen(0)
    display.rectangle(38+3, 122+3, 5, 3)
    display.pen(15)
    display.pixel(41+3, 123+3)
    
    display.pen(0)
    display.rectangle(148, 122+3, 4, 4)
    display.pen(15)
    display.rectangle(148, 122+5, 2, 2)
    display.rectangle(148+2, 122, 4, 4)

    
# switches between modes
def mode(photo_mode, show_QR, photos_taken):
    if photo_mode:
        mode2(show_QR, photos_taken)
    else:
        mode1(show_QR)
        
def update_runner(changed, changed_QR, changed_tally, photos_taken):
    if changed_QR:
        display.update_speed(0) # partial_update only works on update_speed zero
        display.partial_update(198, 40, 96, 96)
        display.update_speed(2)
    elif changed_tally:
        display.update_speed(0)
        display.partial_update(135, 96, 60, 32)
        with open("photos.txt", 'w') as file: 
            file.write(str(photos_taken))
        display.update_speed(2)
    else:
        display.update()
    

changed = True
inverted = False
show_QR = False
changed_QR = False
changed_tally = False
photo_mode = False

with open("photos.txt", 'r') as file: 
    photos_taken = int(file.read())

while True: 
    if display.pressed(badger2040.BUTTON_A):
        if inverted:
            inverted = False
        else:
            inverted = True
        changed = True

    if display.pressed(badger2040.BUTTON_B):
        if show_QR:
            show_QR = False
        else:
            show_QR = True
        changed = True
        changed_QR = True
        
    if display.pressed(badger2040.BUTTON_C):
        if photo_mode:
            photo_mode = False
        else:
            photo_mode = True
        changed = True
        
    if photo_mode and display.pressed(badger2040.BUTTON_UP):
        photos_taken += 1
        changed = True
        changed_tally = True
        
    if photo_mode and display.pressed(badger2040.BUTTON_DOWN):
        photos_taken -= 1
        changed = True
        changed_tally = True
    
    if changed:
        display.invert(inverted)
        mode(photo_mode, show_QR, photos_taken)
        update_runner(changed, changed_QR, changed_tally, photos_taken)
        
        changed = False
        changed_QR = False
        changed_tally = False
        
    display.halt()

