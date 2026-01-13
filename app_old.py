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
        position: relative;
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
        transition: all 0.2s ease;
        position: relative;
        z-index: 2;
    }
    .task-box:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        border-color: #009ee0;
        transform: translateY(-2px);
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
        display: flex;
        align-items: center;
    }
    .avatar {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background-color: #009ee0;
        display: inline-block;
        margin-right: 8px;
    }
    .system-badge {
        background-color: #f15a22;
        color: white;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 11px;
        margin-right: 6px;
        margin-bottom: 6px;
        display: inline-block;
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
    .iteration-bar {
        position: absolute;
        height: 48px;
        border-radius: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 16px;
        z-index: 20;
        box-shadow: 0 6px 18px rgba(0,0,0,0.3);
        padding: 0 32px;
        backdrop-filter: blur(8px);
        opacity: 0.96;
        border: 2px solid rgba(255,255,255,0.3);
    }
    .iterations-panel {
    position: relative;
    height: 220px;          /* УВЕЛИЧИЛИ ВЫСОТУ ПАНЕЛИ — теперь места хватит с запасом */
    margin-top: 40px;
    overflow-x: auto;
    white-space: nowrap;
    background-color: rgba(255,255,255,0.95);
    border-top: 2px solid #e0e0e0;
    padding-top: 20px;
    box-shadow: 0 -4px 12px rgba(0,0,0,0.05);
    }
    .connection-line {
        position: absolute;
        background-color: #009ee0;
        opacity: 0.7;
        pointer-events: none;
        z-index: 1;
    }
    .horizontal-line {
        height: 3px;
    }
    .vertical-line {
        width: 3px;
    }
    .iteration-bar {
    position: absolute;
    height: 52px;
    border-radius: 26px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: bold;
    font-size: 17px;
    z-index: 20;
    box-shadow: 0 8px 20px rgba(0,0,0,0.25);
    padding: 0 36px;
    backdrop-filter: blur(10px);
    opacity: 0.92;
    border: 3px solid rgba(255,255,255,0.4);
    transition: all 0.3s ease;
    }
    .iteration-bar:hover {
    opacity: 1;
    transform: translateY(-4px);
    box-shadow: 0 12px 28px rgba(0,0,0,0.3);
    }
    </style>
""", unsafe_allow_html=True)

# Списки персонала и систем
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

# Инициализация состояния (без изменений)
if 'stages' not in st.session_state:
    st.session_state.stages = [
        "Сквозной сценарий повышения эффективности базовой добычи ДО Хантос",
        "Анализ гипотез повышения эффективности базовой добычи",
        "Актуализация цифровых двойников рассматриваемых активов",
        "Интегрированные расчёты на целевых активах",
        "Митигация рисков осложнений"
    ]
    st.session_state.tasks = {stage: [] for stage in st.session_state.stages}
    # Начальные задачи — оставлены как в оригинале
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
    for name in ["Подбор ГТМ на добывающем фонде на целевых активах",
                 "Подбор ГТМ на нагнетательном фонде на целевых активах", "Оптимизация проектного фонда"]:
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

if 'editing_task' not in st.session_state:
    st.session_state.editing_task = None
if 'editing_stage' not in st.session_state:
    st.session_state.editing_stage = None
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = "Подробный вид"
if 'expanded_states' not in st.session_state:
    st.session_state.expanded_states = {}
if 'matrix_mode' not in st.session_state:
    st.session_state.matrix_mode = False
if 'connections' not in st.session_state:
    st.session_state.connections = []


# Функции для матрицы, экспорта и импорта — без изменений
def get_all_tasks():
    tasks = []
    for i, stage in enumerate(st.session_state.stages):
        for j, task in enumerate(st.session_state.tasks[stage]):
            label = f"{task['id']} — {task['name'][:50]}{'...' if len(task['name']) > 50 else ''}"
            tasks.append(((i, j), label))
    return tasks


all_tasks_list = get_all_tasks()


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


def generate_connections_excel():
    data = []
    for (src_i, src_j), (dst_i, dst_j) in st.session_state.connections:
        src_task = st.session_state.tasks[st.session_state.stages[src_i]][src_j]
        dst_task = st.session_state.tasks[st.session_state.stages[dst_i]][dst_j]
        data.append({
            "Источник ID": src_task['id'],
            "Источник Название": src_task['name'],
            "Источник Этап": st.session_state.stages[src_i],
            "Приёмник ID": dst_task['id'],
            "Приёмник Название": dst_task['name'],
            "Приёмник Этап": st.session_state.stages[dst_i]
        })
    df = pd.DataFrame(data)
    output = BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)
    return output.getvalue()


def load_connections_from_excel(df):
    if df.empty:
        return
    new_connections = []
    task_map = {}
    for i, stage in enumerate(st.session_state.stages):
        for j, task in enumerate(st.session_state.tasks[stage]):
            task_map[task['id']] = (i, j)
    for _, row in df.iterrows():
        src_id = str(row["Источник ID"])
        dst_id = str(row["Приёмник ID"])
        if src_id in task_map and dst_id in task_map:
            new_connections.append((task_map[src_id], task_map[dst_id]))
    st.session_state.connections = new_connections


def load_board_from_excel(df):
    if df.empty:
        st.error("Файл пустой.")
        return False
    required = ["Этап ID", "Этап Название", "Карточка ID", "Карточка Название", "Исполнитель", "Согласующий",
                "Срок сдачи", "Статус", "Дата создания", "Используемые системы"]
    if not all(col in df.columns for col in required):
        st.error("Файл не соответствует структуре доски.")
        return False
    new_stages = []
    new_tasks = {}
    for stage_name in df["Этап Название"].unique():
        new_stages.append(stage_name)
        new_tasks[stage_name] = []
    for _, row in df.iterrows():
        stage = row["Этап Название"]
        systems = [s.strip() for s in str(row["Используемые системы"]).split(",") if
                   s.strip() and s.strip() != "nan"] if pd.notna(row["Используемые системы"]) else []
        task = {
            'id': str(row["Карточка ID"]),
            'name': str(row["Карточка Название"]),
            'executor': str(row["Исполнитель"]),
            'approver': str(row["Согласующий"]),
            'deadline': pd.to_datetime(row["Срок сдачи"]).date() if pd.notna(
                row["Срок сдачи"]) else datetime.now().date(),
            'status': str(row["Статус"]),
            'systems': systems,
            'date': str(row["Дата создания"])
        }
        new_tasks[stage].append(task)
    st.session_state.stages = new_stages
    st.session_state.tasks = new_tasks
    st.session_state.connections = []
    return True


# Верхняя панель
st.markdown("<div class='top-bar'>", unsafe_allow_html=True)
col_left, col_right = st.columns([7, 3])
with col_left:
    st.markdown("<div class='top-left'>", unsafe_allow_html=True)
    st.button("← Назад")
    st.markdown("<h2 style='margin:0 20px 0 0;display:inline;'>Планировщик производственных задач</h2>",
                unsafe_allow_html=True)
    st.markdown("<h3 style='margin:0;display:inline;color:#666;'>ООО \"Газпромнефть-Хантос\" \\ Зимнее</h3>",
                unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
with col_right:
    board_file = st.file_uploader("Загрузить структуру доски", type=["xlsx"], key="board_upload")
    if board_file is not None:
        if st.button("Применить структуру доски"):
            try:
                df = pd.read_excel(board_file)
                if load_board_from_excel(df):
                    st.success("Структура доски обновлена!")
                    st.rerun()
            except Exception as e:
                st.error(f"Ошибка: {e}")
    st.download_button("Выгрузить структуру доски", data=generate_excel(), file_name="tasks_board.xlsx")
    st.download_button("Выгрузить связи", data=generate_connections_excel(), file_name="connections.xlsx")
    connections_file = st.file_uploader("Загрузить связи", type=["xlsx"], key="conn_upload")
    if connections_file is not None:
        if st.button("Применить связи"):
            try:
                df = pd.read_excel(connections_file)
                load_connections_from_excel(df)
                st.success("Связи обновлены!")
                st.rerun()
            except Exception as e:
                st.error(f"Ошибка загрузки связей: {e}")
    st.markdown('<div class="avatar"></div>', unsafe_allow_html=True)
    st.markdown("<div style='text-align:right;'><strong>Сюндюков АВ</strong><br><small>Ведущий эксперт</small></div>",
                unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Контролы
c1, c2, c3, c4, c5, c6, c7 = st.columns([1.5, 1, 2, 2, 1, 1, 2])
with c1:
    st.text_input("Поиск")
with c2:
    st.button("Фильтры")
with c3:
    view_mode = st.radio("Вид", ["Упрощенный вид", "Подробный вид"],
                         index=0 if st.session_state.view_mode == "Упрощенный вид" else 1, horizontal=True)
    if view_mode != st.session_state.view_mode:
        st.session_state.view_mode = view_mode
        expand = view_mode == "Подробный вид"
        for key in st.session_state.expanded_states:
            st.session_state.expanded_states[key] = expand
        st.rerun()
with c4:
    if st.button("Настроить связи"):
        st.session_state.matrix_mode = not st.session_state.matrix_mode
        st.rerun()
with c5:
    st.button("Онтология")
with c6:
    if st.button("+ Добавить этап"):
        st.session_state.stages.insert(0, "Новый этап")
        st.session_state.tasks["Новый этап"] = []
        st.session_state.editing_stage = 0
        st.rerun()
with c7:
    st.button("Рассчитать")

st.markdown("## ВЗАИМОСВЯЗИ ЭТАПОВ")

# Матрица связей
if st.session_state.matrix_mode:
    st.markdown("### Матрица зависимостей задач")
    st.info("Отметьте галочками зависимости (строка → столбец). Можно связывать любые задачи.")

    task_ids = [t[0] for t in all_tasks_list]
    task_labels = [t[1] for t in all_tasks_list]

    matrix_data = {}
    for src_label in task_labels:
        matrix_data[src_label] = {dst_label: False for dst_label in task_labels}

    for (src_pos, dst_pos) in st.session_state.connections:
        src_label = all_tasks_list[task_ids.index(src_pos)][1]
        dst_label = all_tasks_list[task_ids.index(dst_pos)][1]
        matrix_data[src_label][dst_label] = True

    matrix_df = pd.DataFrame(matrix_data).T

    edited_df = st.data_editor(
        matrix_df,
        use_container_width=True,
        column_config={col: st.column_config.CheckboxColumn(col, default=False) for col in matrix_df.columns},
        hide_index=False,
        num_rows="fixed"
    )

    new_connections = []
    for src_label, row in edited_df.iterrows():
        for dst_label, checked in row.items():
            if checked and src_label != dst_label:
                src_idx = task_labels.index(src_label)
                dst_idx = task_labels.index(dst_label)
                src_pos = task_ids[src_idx]
                dst_pos = task_ids[dst_idx]
                new_connections.append((src_pos, dst_pos))

    if new_connections != st.session_state.connections:
        st.session_state.connections = new_connections
        st.rerun()

# Основная доска — теперь без большого padding-top
st.markdown("<div style='position: relative; overflow-x: auto; white-space: nowrap; padding-bottom: 20px;'>",
            unsafe_allow_html=True)

# Генерация итераций — 2 итерация (левые 3), 3 итерация (центр), 2 итерация (правые 3) — с сильным разносом по высоте
if 'iterations' not in st.session_state:
    st.session_state.iterations = []
    num_stages = len(st.session_state.stages)

    stage_width = 340
    padding_per_side = 50

    # 1. Левая плашка: "2 итерация" — первые 3 этапа
    start1 = 0
    end1 = min(3, num_stages)
    if end1 - start1 >= 2:
        span1 = end1 - start1
        width1 = span1 * stage_width - 2 * padding_per_side
        left1 = start1 * stage_width + (span1 * stage_width - width1) / 2
        st.session_state.iterations.append({
            'width': max(width1, 260),
            'left': left1,
            'color': '#4ECDC4',
            'label': '2 итерация',
            'top': 20          # самая верхняя
        })

    # 2. Центральная плашка: "3 итерация" — центр, 3–4 этапа
    center_start = max(0, (num_stages // 2) - 2)
    center_end = min(num_stages, center_start + 4)
    if center_end - center_start < 3:
        center_end = min(num_stages, center_start + 3)
    if center_end - center_start >= 2:
        span2 = center_end - center_start
        width2 = span2 * stage_width - 2 * padding_per_side
        left2 = center_start * stage_width + (span2 * stage_width - width2) / 2
        # Немного сдвигаем влево/вправо случайно — чтобы не была строго под первой/третьей
        left2 += random.choice([-30, 30])
        st.session_state.iterations.append({
            'width': max(width2, 300),
            'left': left2,
            'color': '#FFD166',
            'label': '3 итерация',
            'top': 80          # сильно ниже первой
        })

    # 3. Правая плашка: "2 итерация" — последние 3 этапа
    start3 = max(0, num_stages - 3)
    end3 = num_stages
    if end3 - start3 >= 2:
        span3 = end3 - start3
        width3 = span3 * stage_width - 2 * padding_per_side
        left3 = start3 * stage_width + (span3 * stage_width - width3) / 2
        st.session_state.iterations.append({
            'width': max(width3, 260),
            'left': left3,
            'color': '#FF6B6B',
            'label': '2 итерация',
            'top': 140         # ещё ниже — полный разнос
        })

# Отрисовка связей (в основной доске)
for (src_stage_idx, src_task_idx), (dst_stage_idx, dst_task_idx) in st.session_state.connections:
    src_x = src_stage_idx * 340 + 170
    dst_x = dst_stage_idx * 340 + 170
    src_y = 160 + src_task_idx * 140 + 80
    dst_y = 160 + dst_task_idx * 140 + 80
    mid_y = max(src_y, dst_y) + 70
    st.markdown(f"""
        <div class="connection-line horizontal-line"
             style="left:{min(src_x, dst_x)}px; top:{mid_y}px; width:{abs(dst_x - src_x)}px;"></div>
        <div class="connection-line vertical-line"
             style="left:{src_x}px; top:{min(src_y, mid_y)}px; height:{abs(mid_y - src_y)}px;"></div>
        <div class="connection-line vertical-line"
             style="left:{dst_x}px; top:{min(dst_y, mid_y)}px; height:{abs(mid_y - dst_y)}px;"></div>
    """, unsafe_allow_html=True)

# Колонки этапов
cols = st.columns(len(st.session_state.stages))
for i, stage in enumerate(st.session_state.stages):
    with cols[i]:
        st.markdown(f"<div class='stage-column'>", unsafe_allow_html=True)
        header_left, header_right = st.columns([4, 1])
        with header_left:
            if st.session_state.editing_stage == i:
                new_name = st.text_input("Название этапа", value=stage, key=f"stage_name_{i}")
                if st.button("Сохранить"):
                    old_name = stage
                    st.session_state.stages[i] = new_name
                    st.session_state.tasks[new_name] = st.session_state.tasks.pop(old_name)
                    st.session_state.editing_stage = None
                    st.rerun()
            else:
                st.markdown(f"<div class='stage-header'>{stage}</div>", unsafe_allow_html=True)
        with header_right:
            st.markdown("<div class='stage-arrows'>", unsafe_allow_html=True)
            if i > 0:
                if st.button("←", key=f"stage_left_{i}"):
                    st.session_state.stages[i - 1], st.session_state.stages[i] = st.session_state.stages[i], \
                                                                                 st.session_state.stages[i - 1]
                    st.rerun()
            if i < len(st.session_state.stages) - 1:
                if st.button("→", key=f"stage_right_{i}"):
                    st.session_state.stages[i], st.session_state.stages[i + 1] = st.session_state.stages[i + 1], \
                                                                                 st.session_state.stages[i]
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        for j, task in enumerate(st.session_state.tasks[stage]):
            key = f"expander_{i}_{j}"
            if key not in st.session_state.expanded_states:
                st.session_state.expanded_states[key] = st.session_state.view_mode == "Подробный вид"
            expanded = st.session_state.expanded_states[key]
            with st.expander(f"{task['id']} — {task['name']}", expanded=expanded):
                st.markdown(f"<div class='task-box'>", unsafe_allow_html=True)
                if st.session_state.editing_task == (i, j):
                    new_name = st.text_input("Название задачи", value=task['name'])
                    new_executor = st.selectbox("Исполнитель", personnel, index=personnel.index(task['executor']))
                    new_approver = st.selectbox("Согласующий", personnel, index=personnel.index(task['approver']))
                    new_deadline = st.date_input("Срок сдачи", value=task['deadline'])
                    new_status = st.selectbox("Статус", ["в работе", "завершен", "ошибка"],
                                              index=["в работе", "завершен", "ошибка"].index(task['status']))
                    new_systems = st.multiselect("Используемые системы", systems_list, default=task['systems'])
                    col_save, col_cancel = st.columns(2)
                    with col_save:
                        if st.button("Сохранить", key=f"save_{i}_{j}"):
                            task['name'] = new_name
                            task['executor'] = new_executor
                            task['approver'] = new_approver
                            task['deadline'] = new_deadline
                            task['status'] = new_status
                            task['systems'] = new_systems
                            st.session_state.editing_task = None
                            st.rerun()
                    with col_cancel:
                        if st.button("Отмена", key=f"cancel_{i}_{j}"):
                            st.session_state.editing_task = None
                            st.rerun()
                else:
                    status_map = {'завершен': 'green', 'ошибка': 'red', 'в работе': 'blue'}
                    st.markdown(f"<span class='status-badge {status_map[task['status']]}'>{task['status']}</span>",
                                unsafe_allow_html=True)
                    st.markdown(f"<div class='task-detail'><strong>Срок:</strong> {task['deadline']}</div>",
                                unsafe_allow_html=True)
                    st.markdown(
                        f"<div class='task-detail'><strong>Исполнитель:</strong> <div class='avatar'></div>{task['executor']}</div>",
                        unsafe_allow_html=True)
                    st.markdown(
                        f"<div class='task-detail'><strong>Согласующий:</strong> <div class='avatar'></div>{task['approver']}</div>",
                        unsafe_allow_html=True)
                    st.markdown("<div class='task-detail'><strong>Системы:</strong></div>", unsafe_allow_html=True)
                    for sys in task['systems']:
                        st.markdown(f"<span class='system-badge'>{sys}</span>", unsafe_allow_html=True)
                    st.markdown("<div class='task-detail'><strong>Выходные данные:</strong></div>",
                                unsafe_allow_html=True)
                    st.markdown("<a href='https://google.com' target='_blank'>📄 Результаты расчета</a>",
                                unsafe_allow_html=True)
                    if st.button("Редактировать", key=f"edit_{i}_{j}"):
                        st.session_state.editing_task = (i, j)
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
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

# === НОВАЯ ПАНЕЛЬ С ИТЕРАЦИЯМИ ВНИЗУ СТРАНИЦЫ ===
st.markdown("<div class='iterations-panel'>", unsafe_allow_html=True)
st.markdown("<h4 style='margin-left: 20px; color: #444;'>Итерации</h4>", unsafe_allow_html=True)

# Отрисовка плашек итераций в нижней панели
for it in st.session_state.iterations:
    st.markdown(f"""
        <div class="iteration-bar" style="top: {it['top']}px; width: {it['width']}px; left: {it['left']}px; background-color: {it['color']};">
            {it['label']}
        </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)