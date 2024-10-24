from nicegui import ui, app, tailwind
import models as md

taskCard = False


def add_task(task):
    md.insert_task(task)
    ui.navigate.to(main_page, new_tab=False)


def update_parameter(task, value, parameter):
    task[parameter] = value


def update_task(edit_task_id, task):
    md.update_task(edit_task_id, task)
    ui.navigate.to(main_page, new_tab=False)


@ui.page('/task_form')
def task_form():
    task = {}

    if 'task' in app.storage.general:
        edit_task = app.storage.general['task']

        titulo = edit_task.titulo
        descripcion = edit_task.descripcion
        fecha_vencimiento = edit_task.fecha_vencimiento
        categoria = edit_task.categoria

    else:
        titulo = ''
        descripcion = ''
        fecha_vencimiento = ''
        categoria = ''


    with ui.card().style('width: 400px'):
        ui.label('Nueva tarea').style('color: #6E93D6; font-size: 200%; font-weight: 300')

        ui.input(label='Titulo', value=titulo, on_change=lambda e: update_parameter(task, e.value, 'titulo'), validation={'Input too long': lambda value: len(value) < 30})

        ui.textarea(label='Descripcion', value=descripcion, on_change=lambda e: update_parameter(task, e.value, 'descripcion'))

        with ui.input(label='Fecha de vencimiento', value=fecha_vencimiento, on_change=lambda e: update_parameter(task, e.value, 'fecha_vencimiento')) as date:
            with ui.menu().props('no-parent-event') as menu:
                with ui.date().bind_value(date):
                    with ui.row().classes('justify-end'):
                        ui.button('Close', on_click=menu.close).props('flat')
            with date.add_slot('append'):
                ui.icon('edit_calendar').on('click', menu.open).classes('cursor-pointer')


        with ui.dropdown_button('Prioridad', auto_close=True):
            ui.item('Alta', on_click=lambda: update_parameter(task, 'alta', 'prioridad'))
            ui.item('Media', on_click=lambda: update_parameter(task, 'media', 'prioridad'))
            ui.item('Baja', on_click=lambda: update_parameter(task, 'baja', 'prioridad'))

        ui.input(label='Categoria', value=categoria, on_change=lambda e: update_parameter(task, e.value, 'categoria'), validation={'Input too long': lambda value: len(value) < 20})

        with ui.row():
            if 'task' in app.storage.general:
                ui.button(icon='add', on_click=lambda: update_task(edit_task.id, task)).props('fab color=accent')

                del app.storage.general['task']
            else:
                ui.button(icon='add', on_click=lambda: add_task(task)).props('fab color=accent')
                
            ui.button(icon='undo', on_click=lambda: ui.navigate.to(main_page, new_tab=False)).props('fab color=accent').style('position: absolute; right: 0px; margin-right: 10px;')


def edit_task(task):
    app.storage.general['task'] = task
    ui.navigate.to(task_form, new_tab=False)


def delete_task(task):
    md.delete_task(task.id)
    ui.navigate.to(main_page, new_tab=False)


class TaskCard():
    task = None

    def create_taskRow(self):
        with ui.row().classes('flex flex-nowrap bg-primary text-primary-content w-full py-8 items-center rounded-md text-white my-2 shadow-lg'):
            ui.checkbox(on_change=lambda e: md.change_completed_task(self.task.id, e.value)).classes('checkbox w-1/12')
            ui.label(self.task.titulo).classes('w-9/12')
            with ui.row():
                ui.button(icon='edit', on_click=lambda: edit_task(self.task)).props('fab color=accent')
                ui.button(icon='delete', on_click=lambda: delete_task(self.task)).props('fab color=accent')

    def create_taskCard(self):
        with ui.card().classes('card bg-primary text-primary-content w-full text-white my-2 shadow-lg'):
            with ui.row().classes('flex flex-nowrap w-full items-center'):
                ui.checkbox(on_change=lambda e: md.change_completed_task(self.task.id, e.value)).classes('checkbox w-1/12')
                ui.label(self.task.titulo).classes('w-9/12')
                ui.label(self.task.fecha_vencimiento)

            ui.label(self.task.descripcion)
            ui.label(self.task.prioridad)
            ui.label(self.task.categoria)
                
            with ui.row().classes('place-self-end items-center m-4'):
                ui.button(icon='edit', on_click=lambda: edit_task(self.task)).props('fab color=accent')
                ui.button(icon='delete', on_click=lambda: delete_task(self.task)).props('fab color=accent')
                


@ui.refreshable
def update_list():
    tasks = md.select_task()

    if tasks:
        with ui.list().props('dense separator').classes('w-full'):
            for task in tasks:
                task_card = TaskCard()

                task_card.task = task

                if taskCard:
                    task_card.create_taskCard()
                else:
                    task_card.create_taskRow()


def change_task_list(value):
    global taskCard
    taskCard = value

    ui.navigate.to(main_page, new_tab=False)


@ui.page('/')
def main_page():

    with ui.card().classes('card w-full'):
        with ui.row().classes('flex flex-nowrap w-full'):
            ui.label('Lista de tareas').classes('w-11/12').style('color: #6E93D6; font-size: 200%; font-weight: 300')
            ui.button(icon='add', on_click=lambda: ui.navigate.to(task_form, new_tab=False)).props('fab color=accent')

        with ui.button_group():
            ui.button(icon='view_list', on_click=lambda: change_task_list(False))
            ui.button(icon='apps', on_click=lambda: change_task_list(True))
        
        update_list()

ui.run()