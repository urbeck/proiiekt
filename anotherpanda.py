from direct.showbase.ShowBase import ShowBase

game = ShowBase()
base.disableMouse() #отлючает стандартное управление мышью
model = loader.loadModel('models/environment')
model.reparentTo(render)
model.setScale(0.1)

base.accept("escape", base.userExit)
#акцепт - "договор", привязка клавиш к действиям

#создать класс блока
class block():
    def __init__(self, pos):
        self.pos = pos
        kamen = loader.loadModel('block.egg')
        tex = loader.loadTexture('block.png')
        kamen.setTexture(tex)
        kamen.setPos(self.pos)
        kamen.reparentTo(render)


# ставим блоки друг на друга
stroika = list() #список уже поставленных блоков
def postblock():
    x1 = base.camera.getX()
    y1 = base.camera.getY()
    x1 = round(x1, 0) #роунд - округляет число, 0 - значит, убрать дробную часть
    y1 = round(y1, 0)
    n = 0
    if len(stroika) ==0: #если блоков нет - делаем один
        newblock = block((x1,y1,0.5))
    for i in stroika: #перебор-проверка всех блоков
        if i.pos == (x1, y1, 0.5): #если на месте, где стоим, есть блок
            n += 1
            newblock = block((x1,y1,0.5+n)) #ставим новый чуть выше
        else:
            newblock = block((x1,y1,0.5)) #иначе ставим просто блок
    stroika.append(newblock) #добавляем блок к списку построенных

base.accept("b", postblock)


#создаем "договоренности" о клавишах
#делаем большую функцию для обработки действий

keys = dict()
heading =0
pitch = 0

def setKey(key, value):
    keys[key] = value
#назначаем правило: нажата кнопка это 1, отпущена это 0.
for key in ['a','d','w','s']:
    keys[key] = 0
    base.accept(key, setKey, [key, 1])
    base.accept(key+'-up', setKey, [key, 0]) # +"-up" означает отпущенную клавишу

def controlCamera(task):
    step = 0.2 #длина нашего шага
    move_x = step * (keys['d'] - keys['a']) #в зависимости от нажатия кнопок, мы получаем "тягу"
    move_y = step * (keys['w'] - keys['s']) #в ту или иную сторону (0-1 = -1, 1-0 = 1)
    base.camera.setPos(base.camera, move_x,move_y,0) #смещаем камеру в направлении
    zos = 2.5 #устанавливаем камеру на высоту
    base.camera.setZ(zos) #фиксируем героя на высоте (если делать иначе, героя начнёт поднимать вверх)

    global heading, pitch
    mouse_step = 0.2
    new_mouse_pos = base.win.getPointer(0) #ищем где мышь
    new_x = new_mouse_pos.getX()
    new_y = new_mouse_pos.getY()
    centerX = base.win.getXSize()//2#ищем середину экрана, X и Y
    centerY = base.win.getYSize()//2
    if base.win.movePointer(0, centerX,centerY): #мышь ушла из центра экрана
        heading = heading - (new_x - centerX) * mouse_step         # <=== вычисляем углы
        pitch = pitch - (new_y - centerY) * mouse_step
        base.camera.setHpr(heading,pitch,0)#наклоняем и поворачиваем камеру
    base.win.movePointer(0,centerX,centerY) #возвращаем курсор обратно
    return task.again

taskMgr.doMethodLater(0.02, controlCamera, "camera-task")


game.run()