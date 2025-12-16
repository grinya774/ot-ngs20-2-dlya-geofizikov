import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime, timedelta
import random

st.set_page_config(layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #f5f7fa;
        font-family: 'Segoe UI', sans-serif;
        font-size: 13px;
    }
    .stage-column {
        background-color: #ffffff;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
        padding: 16px;
        margin: 0 10px;
        min-width: 300px;
    }
    .stage-header {
        font-weight: 600;
        font-size: 15px;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 2px solid #009ee0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .stage-arrows button {
        background: none;
        border: none;
        font-size: 18px;
        color: #666;
        cursor: pointer;
    }
    .task-box {
        background-color: #ffffff;
        border: 2px solid #d0d0d0;
        border-radius: 8px;
        padding: 14px;
        margin-bottom: 12px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        cursor: grab;
        transition: all 0.2s ease;
    }
    .task-box:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        border-color: #009ee0;
        transform: translateY(-2px);
    }
    .task-id {
        font-weight: 600;
        font-size: 14px;
        color: #009ee0;
        margin-bottom: 8px;
    }
    .task-name {
        font-weight: 500;
        font-size: 14px;
        margin-bottom: 10px;
        line-height: 1.4;
    }
    .status-badge {
        font-size: 11px;
        padding: 4px 8px;
        border-radius: 12px;
        color: white;
        display: inline-block;
        margin-bottom: 10px;
    }
    .green { background-color: #009ee0; }
    .red { background-color: #f15a22; }
    .blue { background-color: #666666; }
    .task-detail {
        font-size: 12px;
        margin-bottom: 6px;
        color: #444;
    }
    .avatar {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background-color: #009ee0;
        display: inline-block;
        vertical-align: middle;
        margin-right: 8px;
    }
    .add-button {
        width: 100%;
        text-align: center;
        padding: 12px;
        background-color: #f8f9fa;
        border: 2px dashed #009ee0;
        border-radius: 8px;
        color: #009ee0;
        font-weight: 500;
        cursor: pointer;
        margin-top: 10px;
    }
    .top-bar {
        background-color: #ffffff;
        padding: 12px 20px;
        border-bottom: 1px solid #e0e0e0;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .top-left {
        display: flex;
        align-items: center;
        gap: 25px;
    }
    .user-info {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# Полные списки
personnel = [
    "Сюндюков А. В.", "Иванова Е. П.", "Петров С. М.", "Сидорова О. И.", "Козлов Д. А.",
    "Николаев Г. Р.", "Макарова В. Л.", "Орлов Н. С.", "Васнецова Т. К.", "Жуков П. Ф.",
    "Алексеева М. Д.", "Тихонов И. Г.", "Павлова А. Н.", "Фролов В. Я.", "Савельев К. О.",
    "Морозова Л. Б.", "Белов Р. Т.", "Комарова Ю. Э.", "Громов Е. Ц.", "Ильина Н. Ч.",
    "Данилов Б. Х.", "Семёнова З. Щ.", "Блинов М. Ю.", "Ларина А. Ж.", "Гордеев И. У."
]

systems_list = [
    "Сервис Микросервис Б6К Расчет ХВ скважин", "Б6К Расчет Кпрод скважин", "Б6К Расчет Pпл скважин",
    "Б6К Расчет запасов скважин", "Спектр spektr-addperforations", "Спектр Расчёт ГРП",
    "Спектр Сервис оптимизации тех параметров", "Спектр Сервис ОПЗ", "Спектр Расчёт проницаемости",
    "Спектр Расчёт восстановления давления", "Спектр Расчёт ПВЛГ", "Спектр Расчёт ВБД",
    "Спектр Расчет ЗБС", "eXoil Адаптация модели пласта на основе метода граничных элементов",
    "eXoil Модель вытеснения на основе линий тока", "eXoil Оптимизатор ППД", "eXoil Проектные скважины",
    "eXoil АТСР", "eXoil Расчет запусконого дебита по скважине",
    "eXoil Адаптация модели пласта на основе метода граничных элементов",
    "eXoil Модель пласта на основе метода граничных элементов",
    "eXoil Модель вытеснения на основе линий тока", "eXoil Оптимизатор ППД",
    "eXoil Проектные скважины", "ГибрИМА Расчёт IPR-кривых", "ГибрИМА Расчёт узлового анализа",
    "ГибрИМА Оптимизатор режимов работы скважин с учётом влияния устьевого давления",
    "ЦД велл Расчет PVT свойств", "ЦД велл Расчет продуктивности",
    "ЦД велл Расчет кривых распределения давления и температуры по стволу (Моделирование VLP)",
    "ЦД велл Расчет узлового анализа", "ЦД велл Расчет анализа чувствительности"
]

# Инициализация с предзаполнением
if 'stages' not in st.session_state:
    st.session_state.stages = [
        "Сквозной сценарий повышения эффективности базовой добычи ДО Хантос",
        "Анализ гипотез повышения эффективности базовой добычи",
        "Актуализация цифровых двойников рассматриваемых активов",
        "Интегрированные расчёты на целевых активах",
        "Митигация рисков осложнений"
    ]
    st.session_state.tasks = {stage: [] for stage in st.session_state.stages}

    # Предзаполнение карточек
    st.session_state.tasks[st.session_state.stages[0]].append({
        'id': 'M14500',
        'name': "Анализ эффективности текущего состояния разработки и эксплуатации актива",
        'executor': random.choice(personnel),
        'approver': random.choice(personnel),
        'deadline': (datetime.now() + timedelta(days=15)).date(),
        'status': 'в работе',
        'systems': random.sample(systems_list, k=random.randint(1, 3)),
        'date': datetime.now().strftime("%d.%m.%Y")
    })
    for name in ["Подбор ГТМ на добывающем фонде на целевых активах", "Подбор ГТМ на нагнетательном фонде на целевых активах", "Оптимизация проектного фонда"]:
        st.session_state.tasks[st.session_state.stages[1]].append({
            'id': f'M{random.randint(14501, 14999)}',
            'name': name,
            'executor': random.choice(personnel),
            'approver': random.choice(personnel),
            'deadline': (datetime.now() + timedelta(days=random.randint(10, 40))).date(),
            'status': random.choice(['в работе', 'завершен', 'ошибка']),
            'systems': random.sample(systems_list, k=random.randint(1, 4)),
            'date': datetime.now().strftime("%d.%m.%Y")
        })
    for name in ["Актуализация модели инфраструктуры", "Актуализация модели скважин", "Актуализация модели пласта"]:
        st.session_state.tasks[st.session_state.stages[2]].append({
            'id': f'M{random.randint(14501, 14999)}',
            'name': name,
            'executor': random.choice(personnel),
            'approver': random.choice(personnel),
            'deadline': (datetime.now() + timedelta(days=random.randint(10, 40))).date(),
            'status': random.choice(['в работе', 'завершен', 'ошибка']),
            'systems': random.sample(systems_list, k=random.randint(1, 4)),
            'date': datetime.now().strftime("%d.%m.%Y")
        })
    st.session_state.tasks[st.session_state.stages[3]].append({
        'id': f'M{random.randint(14501, 14999)}',
        'name': "Интегрированные расчёты на целевых активах",
        'executor': random.choice(personnel),
        'approver': random.choice(personnel),
        'deadline': (datetime.now() + timedelta(days=random.randint(10, 40))).date(),
        'status': 'в работе',
        'systems': random.sample(systems_list, k=random.randint(1, 3)),
        'date': datetime.now().strftime("%d.%m.%Y")
    })
    for name in ["Оценка рисков снижения коэффициента продуктивности из-за выпадения отложений",
                 "Оценка рисков возникновения дополнительных гидравлических сопротивлений за счёт образования органич. и неорганич. отложений в трубах",
                 "Оценка рисков снижения МРП скважинного оборудования"]:
        st.session_state.tasks[st.session_state.stages[4]].append({
            'id': f'M{random.randint(14501, 14999)}',
            'name': name,
            'executor': random.choice(personnel),
            'approver': random.choice(personnel),
            'deadline': (datetime.now() + timedelta(days=random.randint(10, 40))).date(),
            'status': random.choice(['в работе', 'завершен', 'ошибка']),
            'systems': random.sample(systems_list, k=random.randint(1, 4)),
            'date': datetime.now().strftime("%d.%m.%Y")
        })

# Состояние редактирования и создания
if 'editing_task' not in st.session_state:
    st.session_state.editing_task = None  # (stage_index, task_index) или None
if 'creating_task' not in st.session_state:
    st.session_state.creating_task = None  # stage_index или None

def generate_excel():
    data = []
    for s_idx, stage in enumerate(st.session_state.stages, 1):
        for task in st.session_state.tasks[stage]:
            row = {
                "Этап ID": s_idx,
                "Этап Название": stage,
                "Карточка ID": task['id'],
                "Карточка Название": task['name'],
                "Исполнитель": task['executor'],
                "Согласующий": task['approver'],
                "Срок сдачи": task['deadline'],
                "Статус": task['status'],
                "Дата создания": task['date'],
                "Используемые системы": ", ".join(task['systems'])
            }
            data.append(row)
    df = pd.DataFrame(data)
    output = BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)
    return output.getvalue()

# Верхняя панель
st.markdown("<div class='top-bar'>", unsafe_allow_html=True)
col_left, col_right = st.columns([7, 3])
with col_left:
    st.markdown("<div class='top-left'>", unsafe_allow_html=True)
    st.button("← Назад")
    st.markdown("<h2 style='margin:0 20px 0 0;display:inline;'>Планировщик производственных задач</h2>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin:0;display:inline;color:#666;'>ООО \"Газпромнефть-Хантос\" \\ Зимнее</h3>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
with col_right:
    st.download_button("Выгрузить в Excel", data=generate_excel(), file_name="tasks.xlsx")
    st.markdown('<div class="avatar"></div>', unsafe_allow_html=True)
    st.markdown("<div style='text-align:right;'><strong>Сюндюков АВ</strong><br><small>Ведущий эксперт</small></div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Контролы
c1, c2, c3, c4, c5, c6, c7 = st.columns([1.5,1,1,1,1,1,2])
with c1:
    st.text_input("Поиск")
with c2:
    st.button("Фильтры")
with c3:
    st.toggle("Упрощенный вид")
with c4:
    st.toggle("Подробный вид", value=True)
with c5:
    st.button("Онтология")
with c6:
    if st.button("+ Добавить этап"):
        st.session_state.stages.insert(0, "Новый этап")
        st.session_state.tasks["Новый этап"] = []
        st.rerun()
with c7:
    st.button("Рассчитать")

st.markdown("## ВЗАИМОСВЯЗИ ЭТАПОВ")

st.markdown("<div style='overflow-x:auto;white-space:nowrap;padding-bottom:20px;'>", unsafe_allow_html=True)
cols = st.columns(len(st.session_state.stages))

for i, stage in enumerate(st.session_state.stages):
    with cols[i]:
        st.markdown(f"<div class='stage-column'>", unsafe_allow_html=True)
        header_left, header_right = st.columns([4, 1])
        with header_left:
            st.markdown(f"<div class='stage-header'>{stage}</div>", unsafe_allow_html=True)
        with header_right:
            st.markdown("<div class='stage-arrows'>", unsafe_allow_html=True)
            if i > 0:
                if st.button("←", key=f"stage_left_{i}"):
                    st.session_state.stages[i-1], st.session_state.stages[i] = st.session_state.stages[i], st.session_state.stages[i-1]
                    st.rerun()
            if i < len(st.session_state.stages)-1:
                if st.button("→", key=f"stage_right_{i}"):
                    st.session_state.stages[i], st.session_state.stages[i+1] = st.session_state.stages[i+1], st.session_state.stages[i]
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        # Карточки
        for j, task in enumerate(st.session_state.tasks[stage]):
            # Если эта карточка редактируется или создаётся новая
            if st.session_state.editing_task == (i, j) or (st.session_state.creating_task == i and j == len(st.session_state.tasks[stage]) - 1 and st.session_state.editing_task is None):
                with st.form(key=f"form_{i}_{j}"):
                    new_name = st.text_input("Название задачи", value=task['name'])
                    new_executor = st.selectbox("Исполнитель", personnel, index=personnel.index(task['executor']))
                    new_approver = st.selectbox("Согласующий", personnel, index=personnel.index(task['approver']))
                    new_deadline = st.date_input("Срок сдачи", value=task['deadline'])
                    new_status = st.selectbox("Статус", ["в работе", "завершен", "ошибка"], index=["в работе", "завершен", "ошибка"].index(task['status']))
                    new_systems = st.multiselect("Используемые системы", systems_list, default=task['systems'])

                    col_save, col_cancel = st.columns(2)
                    with col_save:
                        if st.form_submit_button("Сохранить"):
                            task['name'] = new_name
                            task['executor'] = new_executor
                            task['approver'] = new_approver
                            task['deadline'] = new_deadline
                            task['status'] = new_status
                            task['systems'] = new_systems
                            st.session_state.editing_task = None
                            st.session_state.creating_task = None
                            st.rerun()
                    with col_cancel:
                        if st.form_submit_button("Отмена"):
                            if st.session_state.creating_task == i:
                                st.session_state.tasks[stage].pop()  # Удалить новую
                            st.session_state.editing_task = None
                            st.session_state.creating_task = None
                            st.rerun()
            else:
                # Обычный вид карточки
                with st.expander(f"{task['id']} — {task['name']}", expanded=False):
                    st.markdown(f"<div class='task-box'>", unsafe_allow_html=True)
                    status_map = {'завершен': 'green', 'ошибка': 'red', 'в работе': 'blue'}
                    st.markdown(f"<span class='status-badge {status_map[task['status']]}'>{task['status']}</span>", unsafe_allow_html=True)
                    st.markdown(f"<div class='task-detail'><strong>Срок:</strong> {task['deadline']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='task-detail'><strong>Исполнитель:</strong> {task['executor']}</div>", unsafe_allow_html=True)
                    st.markdown('<div class="avatar"></div>', unsafe_allow_html=True)
                    st.markdown(f"<div class='task-detail'><strong>Согласующий:</strong> {task['approver']}</div>", unsafe_allow_html=True)
                    st.markdown('<div class="avatar"></div>', unsafe_allow_html=True)
                    st.markdown("<div class='task-detail'><strong>Системы:</strong></div>", unsafe_allow_html=True)
                    for sys in task['systems']:
                        st.markdown(f"<div class='task-detail'>- {sys}</div>", unsafe_allow_html=True)
                    st.markdown("<div class='task-detail'><strong>Выходные данные:</strong></div>", unsafe_allow_html=True)
                    st.markdown("<a href='https://google.com' target='_blank'>📄 Результаты расчета</a>", unsafe_allow_html=True)
                    if st.button("Редактировать", key=f"edit_{i}_{j}"):
                        st.session_state.editing_task = (i, j)
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

        # Добавление новой задачи
        if st.button("+ Добавить задачу", key=f"add_{i}"):
            new_task = {
                'id': f"M{random.randint(15000, 99999)}",
                'name': "Новая задача",
                'executor': personnel[0],
                'approver': personnel[0],
                'deadline': datetime.now().date(),
                'status': "в работе",
                'systems': [],
                'date': datetime.now().strftime("%d.%m.%Y")
            }
            st.session_state.tasks[stage].append(new_task)
            st.session_state.editing_task = (i, len(st.session_state.tasks[stage]) - 1)
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)