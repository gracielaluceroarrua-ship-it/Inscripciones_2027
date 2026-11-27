import requests
import streamlit as st

st.set_page_config(page_title="Inscripciones Inglés 2027", page_icon="📝")

# ==============================================================================
# BLOQUEO TEMPORAL PARA PRUEBAS (Se desactiva borrando CLAVE_PRUEBA en Secrets)
# ==============================================================================
clave_esperada = str(st.secrets.get("CLAVE_PRUEBA", "")).strip()

if clave_esperada:
    if "acceso_autorizado" not in st.session_state:
        st.session_state.acceso_autorizado = False

    if not st.session_state.acceso_autorizado:
        st.title("🔒 Acceso restringido — Modo prueba")
        st.info("Este formulario se encuentra en etapa de revisión interna por el equipo docente.")
        with st.form("form_clave_prueba"):
            clave_ingresada = st.text_input("Ingresá la clave de acceso:", type="password")
            entrar = st.form_submit_button("Ingresar")

        if entrar:
            if clave_ingresada.strip() == clave_esperada:
                st.session_state.acceso_autorizado = True
                st.rerun()
            else:
                st.error("Clave incorrecta.")
        st.stop()
# ==============================================================================

CARRERAS = [
    "Lic. en Cs. Matemáticas (Plan 9/17)",
    "Profesorado en Matemática",
    "Profesorado en Tecnología Electrónica (Plan 05/09)",
    "Tecnicatura Universitaria en Electrónica (Plan 15/13)",
    "Tecnicatura Universitaria en Telecomunicaciones (Plan 16/13)",
    "Ingeniería en Electrónica con Orientación en Sistemas Digitales (Plan 13/08 - OCD-6/24)",
    "Tecnicatura Universitaria en Energías Renovables (Plan 05/13)",
    "Lic. en Física (Plan 15/06)",
    "Prof. en Física (Plan 16/06)",
    "Ingeniería en Computación (Plan 28/12)",
    "Ingeniería en Informática (Plan 26/12 - OCD-2/25)",
    "Prof. en Cs. de la Computación (Plan 35/86)",
    "Tecnicatura Universitaria en Redes de Computadoras (Plan 12/15)",
    "Tecnicatura Universitaria en Web (Plan 08/13)",
    "Tecnicatura Universitaria en Teledetección y Sistemas de Información Geográfica - T-SIG (OCD-13/22)",
    "Lic. en Cs. Geológicas (Plan 02/22)",
    "Ingeniería en Minas (Plan 11/23)",
    "Tecnicatura Universitaria en Explotación Minera",
    "Tecnicatura Universitaria en Minería (Plan 6/15 - Vocacional)",
    "Tecnicatura Universitaria en Obras Viales (Plan 01/18 - Vocacional)",
    "Tecnicatura Universitaria en Fotografía (Plan 15/15 - Vocacional)",
]

CARRERAS_AGRUPADAS = {
    "Lic. en Cs. Geológicas (Plan 02/22)",
    "Ingeniería en Minas (Plan 11/23)",
    "Tecnicatura Universitaria en Obras Viales (Plan 01/18 - Vocacional)",
    "Tecnicatura Universitaria en Explotación Minera",
}

CARRERAS_CUATRIMESTRALES = {
    "Lic. en Cs. Geológicas (Plan 02/22)",
    "Ingeniería en Minas (Plan 11/23)",
    "Tecnicatura Universitaria en Explotación Minera",
    "Tecnicatura Universitaria en Minería (Plan 6/15 - Vocacional)",
    "Tecnicatura Universitaria en Obras Viales (Plan 01/18 - Vocacional)",
    "Profesorado en Matemática",
}

URL_CAMPUS_VIRTUAL = "https://moodle4vz.unsl.edu.ar/moodle/course/view.php?id=1830"

MENSAJE_INICIO_UNICO = (
    "⚠️ **Importante:** Completá este formulario **una sola vez**. Si enviaste tus datos o "
    "tuviste algún inconveniente durante el proceso, **no vuelvas a intentarlo por tu cuenta**: "
    "escribinos primero a **inglesfmn@gmail.com** para que revisemos el problema antes de "
    "volver a intentarlo."
)

MENSAJE_CONOCIMIENTOS_SOLIDOS = (
    "**Importante:** Completá tus datos en el formulario de abajo y hacé clic en **«Enviar registro»** "
    "para dejar asentada tu inscripción.\n\n"
    "Quienes declaren conocimientos sólidos deberán realizar una **instancia diagnóstica** "
    "para determinar su nivel y ofrecerles una experiencia de cursado más provechosa. "
    "Nos pondremos en contacto con vos **a la brevedad** para informarte **día, horario y modalidad**."
)

MENSAJE_CERTIFICADO_INSTITUTO = (
    "**Importante — seguí estos dos pasos para no perder tu lugar:**\n\n"
    "1. **Completá primero tus datos en el formulario de abajo y hacé clic en «Enviar registro»** "
    "para dejar asentada tu inscripción en nuestro sistema.\n"
    "2. **Enviá el certificado de examen internacional o constancia de aprobación de instituto privado** "
    "por correo electrónico a **inglesfmn@gmail.com**.\n\n"
    "📌 **Aclaración:** La aceptación de los certificados o constancias estará sujeta a la "
    "**evaluación del equipo docente** respecto de su **validez y alcance**."
)

MENSAJE_EQUIVALENCIA_OTRA_CARRERA = (
    "Si tenés **Inglés aprobado en otra carrera**, no debés completar este registro: "
    "el camino correspondiente es solicitar la **equivalencia** comunicándote a "
    "**equivalencia.fmn@gmail.com**."
)

MENSAJE_CONFIRMACION_REGULAR = (
    "✅ **¡Inscripción registrada correctamente para Inglés 2027!**\n\n"
    "Ya podés automatricularte en el aula correspondiente del campus virtual de la UNSL:\n"
    f"👉 [Acceder al Campus Virtual (Moodle)]({URL_CAMPUS_VIRTUAL})\n\n"
    "⚠️ **Importante:** La matriculación en el campus está habilitada **únicamente para estudiantes "
    "efectivos de la asignatura** que hayan completado este formulario. El equipo docente verificará "
    "los listados y **dará de baja** a quienes no figuren en nuestros registros de inscripción."
)

MENSAJE_CONFIRMACION_SOLIDOS = (
    "✅ **¡Registro guardado correctamente para Inglés 2027!**\n\n"
    "Nos comunicaremos con vos **a la brevedad** para informarte **día, horario y modalidad** "
    "del examen de diagnóstico."
)

MENSAJE_CONFIRMACION_CERTIFICADO = (
    "✅ **¡Registro guardado correctamente para Inglés 2027!**\n\n"
    "📩 **Recordatorio:** No olvides enviar ahora tu certificado o constancia por correo "
    "electrónico a **inglesfmn@gmail.com** (sujeto a evaluación del equipo docente respecto "
    "de su validez y alcance). Nos comunicaremos con vos **a la brevedad** para indicarte "
    "los pasos a seguir."
)


def obtener_tipo_cursado(carrera: str) -> str:
    return "Cuatrimestral" if carrera in CARRERAS_CUATRIMESTRALES else "Anual"


def obtener_pestana_destino(tiene_certificado: str, carrera: str) -> str:
    if tiene_certificado == "Sí":
        base = "Con_Certificado"
    elif tiene_certificado == "No":
        base = "Inscripcion_Regular"
    else:
        base = "Conocimientos_Solidos"

    if carrera == "Profesorado en Matemática":
        return f"{base}_Prof_Mat"
    if carrera in CARRERAS_AGRUPADAS:
        return f"{base}_Geo_Minas"
    return base


@st.cache_data(ttl=15)
def obtener_horarios_disponibles(url: str, tipo_cursado: str) -> list[str]:
    if not url or not tipo_cursado:
        return []
    try:
        resp = requests.get(url, params={"tipo": tipo_cursado}, timeout=15, allow_redirects=True)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == "ok":
                return [str(h).strip() for h in data.get("horarios", []) if str(h).strip()]
    except Exception:
        pass
    return []


def enviar_a_sheets(payload: dict) -> tuple[bool, str]:
    url = str(st.secrets.get("APPS_SCRIPT_URL", "")).strip()
    if not url:
        st.error("Falta configurar APPS_SCRIPT_URL en Secrets.")
        return False, "error"
    try:
        resp = requests.post(url, json=payload, timeout=15, allow_redirects=True)
        if resp.status_code == 200:
            try:
                data = resp.json()
                if data.get("status") == "ok":
                    return True, "ok"
                if data.get("status") == "cupo_lleno":
                    obtener_horarios_disponibles.clear()
                    st.warning(data.get("message", "El horario seleccionado completó su cupo."))
                    return False, "cupo_lleno"
                st.error(f"Error en Apps Script: {data.get('message')}")
                return False, "error"
            except ValueError:
                st.error("Respuesta inválida del servidor. Verificá los permisos de la Web App.")
                return False, "error"
        st.error(f"Error HTTP {resp.status_code} al conectar con la planilla.")
        return False, "error"
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return False, "error"


st.title("📝 Registro de Inscripciones — Inglés 2027")
st.write("Respondé las siguientes preguntas para completar tu registro en la asignatura.")
st.warning(MENSAJE_INICIO_UNICO)

# PASO 1: ¿Estás en TFA?
en_tfa = st.radio(
    "1. ¿Estás cursando actualmente el Trayecto de Formación de Apoyo (TFA)?",
    ["Seleccionar...", "Sí", "No"],
)

# ------------------------------------------------------------------------------
# RAMA A: ESTÁ EN TFA (Sí)
# ------------------------------------------------------------------------------
if en_tfa == "Sí":
    st.subheader("Situación académica: TFA en curso")
    st.warning(
        "📌 **Aviso importante:** Mientras estés cursando el **TFA**, no podés inscribirte "
        "ni cursar Inglés.\n\n"
        "1. **Antes de salir, completá tus datos y hacé clic en el botón «Registrar mi consulta»** "
        "que figura aquí abajo para dejar asentada tu situación.\n"
        "2. Una vez que apruebes el TFA, escribinos a **inglesfmn@gmail.com** con el asunto "
        "**`aprobé el TFA`** para coordinar cómo continuar. ¡Muchos éxitos!"
    )

    apellido_tfa = st.text_input("Apellido", key="apellido_tfa")
    nombre_tfa = st.text_input("Nombre", key="nombre_tfa")
    dni_tfa = st.text_input("DNI sin puntos (opcional)", key="dni_tfa")
    email_tfa = st.text_input("Correo electrónico (opcional)", key="email_tfa")
    carrera_tfa = st.selectbox("Seleccioná tu carrera", ["Seleccionar..."] + CARRERAS, key="carrera_tfa")

    if st.button("Registrar mi consulta", type="primary"):
        if not (apellido_tfa.strip() and nombre_tfa.strip()) or carrera_tfa == "Seleccionar...":
            st.warning("Por favor, completá Apellido, Nombre y Carrera antes de registrar tu consulta.")
        else:
            with st.spinner("Registrando..."):
                ok, _ = enviar_a_sheets({
                    "pestana": "TFA",
                    "apellido": apellido_tfa.strip(),
                    "nombre": nombre_tfa.strip(),
                    "dni": dni_tfa.strip(),
                    "email": email_tfa.strip(),
                    "carrera": carrera_tfa,
                    "horario": "",
                })
                if ok:
                    st.success("✅ Consulta registrada correctamente. Recordá escribirnos cuando apruebes el TFA.")

# ------------------------------------------------------------------------------
# RAMA B: NO ESTÁ EN TFA (No)
# ------------------------------------------------------------------------------
elif en_tfa == "No":
    st.subheader("2. Antecedentes en el idioma")
    tiene_certificado = st.radio(
        "¿Poseés certificado internacional vigente, constancia de instituto privado o Inglés aprobado en otra carrera?",
        [
            "Seleccionar...",
            "Sí",
            "No",
            "No, pero poseo conocimientos sólidos de inglés",
        ],
    )

    if tiene_certificado != "Seleccionar...":
        mostrar_formulario = False

        if tiene_certificado == "Sí":
            tipo_antecedente = st.radio(
                "Indicá cuál es tu situación:",
                [
                    "Seleccionar...",
                    "Certificado de examen internacional o constancia de instituto privado",
                    "Inglés aprobado en otra carrera",
                ],
                key="tipo_antecedente",
            )
            if tipo_antecedente == "Certificado de examen internacional o constancia de instituto privado":
                st.info(f"ℹ️ {MENSAJE_CERTIFICADO_INSTITUTO}")
                mostrar_formulario = True
            elif tipo_antecedente == "Inglés aprobado en otra carrera":
                st.warning(f"📌 {MENSAJE_EQUIVALENCIA_OTRA_CARRERA}")
                mostrar_formulario = False

        elif tiene_certificado == "No":
            mostrar_formulario = True

        else:  # "No, pero poseo conocimientos sólidos de inglés"
            st.info(f"ℹ️ {MENSAJE_CONOCIMIENTOS_SOLIDOS}")
            mostrar_formulario = True

        if mostrar_formulario:
            st.subheader("3. Datos personales, carrera y horario")
            apellido = st.text_input("Apellido", key="apellido_no_tfa")
            nombre = st.text_input("Nombre", key="nombre_no_tfa")
            dni = st.text_input("DNI (sin puntos)", key="dni_no_tfa")
            email = st.text_input("Correo electrónico", key="email_no_tfa")
            carrera = st.selectbox("Seleccioná tu carrera", ["Seleccionar..."] + CARRERAS, key="carrera_no_tfa")

            if carrera != "Seleccionar...":
                tipo_cursado = obtener_tipo_cursado(carrera)
                st.caption(f"Tipo de cursado para la selección de horarios: **{tipo_cursado}**")

                url_script = str(st.secrets.get("APPS_SCRIPT_URL", "")).strip()
                horarios_disp = obtener_horarios_disponibles(url_script, tipo_cursado)

                col_h, col_btn = st.columns([4, 1])
                with col_btn:
                    st.write("")
                    st.write("")
                    if st.button("🔄 Actualizar", help="Actualizar cupos disponibles"):
                        obtener_horarios_disponibles.clear()
                        st.rerun()

                with col_h:
                    if horarios_disp:
                        horario_elegido = st.selectbox(
                            "Seleccioná una opción de horario de cursado",
                            ["Seleccionar..."] + horarios_disp,
                            key=f"horario_{tipo_cursado}",
                        )
                    else:
                        horario_elegido = None
                        st.warning(
                            f"⚠️ No hay horarios con cupo disponible para cursado **{tipo_cursado.lower()}** "
                            "en este momento. Consultá con la cátedra a **inglesfmn@gmail.com**."
                        )
            else:
                tipo_cursado = ""
                horarios_disp = []
                horario_elegido = None

            if tiene_certificado == "Sí":
                mensaje_exito = MENSAJE_CONFIRMACION_CERTIFICADO
            elif tiene_certificado == "No":
                mensaje_exito = MENSAJE_CONFIRMACION_REGULAR
            else:
                mensaje_exito = MENSAJE_CONFIRMACION_SOLIDOS

            if st.button("Enviar registro", type="primary"):
                if carrera == "Seleccionar...":
                    st.warning("Por favor, seleccioná tu carrera antes de enviar.")
                elif not horarios_disp:
                    st.warning(
                        f"No hay cupos disponibles para cursado {tipo_cursado.lower()} en este momento."
                    )
                elif (
                    not (apellido.strip() and nombre.strip() and dni.strip() and email.strip())
                    or not horario_elegido
                    or horario_elegido == "Seleccionar..."
                ):
                    st.warning(
                        "Por favor, completá Apellido, Nombre, DNI (sin puntos), Correo electrónico "
                        "y Horario antes de enviar."
                    )
                else:
                    pestana_destino = obtener_pestana_destino(tiene_certificado, carrera)
                    with st.spinner("Guardando registro..."):
                        ok, estado = enviar_a_sheets({
                            "pestana": pestana_destino,
                            "apellido": apellido.strip(),
                            "nombre": nombre.strip(),
                            "dni": dni.strip(),
                            "email": email.strip(),
                            "carrera": carrera,
                            "horario": horario_elegido,
                        })
                        if ok:
                            obtener_horarios_disponibles.clear()
                            st.success(mensaje_exito)
                        elif estado == "cupo_lleno":
                            st.rerun()
