import requests
import streamlit as st

st.set_page_config(page_title="Inscripciones Inglés 2027", page_icon="📝")

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

MENSAJE_CONOCIMIENTOS_SOLIDOS = (
    "Quienes declaren conocimientos sólidos deberán realizar una **instancia diagnóstica** "
    "para determinar su nivel y ofrecerles una experiencia de cursado más provechosa. "
    "Nos pondremos en contacto con vos **a la brevedad** para informarte **fecha y modalidad**."
)

MENSAJE_CERTIFICADO_INSTITUTO = (
    "Si contás con un **certificado de examen internacional** o **constancia de aprobación "
    "de inglés en un instituto privado**, debés enviarla por correo electrónico a "
    "**inglesfmn@gmail.com**.\n\n"
    "📌 **Aclaración:** La aceptación de los certificados o constancias estará sujeta a la "
    "**evaluación del equipo docente** respecto de su **validez y alcance**."
)

MENSAJE_EQUIVALENCIA_OTRA_CARRERA = (
    "Si tenés **Inglés aprobado en otra carrera**, no debés completar este registro: "
    "el camino correspondiente es solicitar la **equivalencia** comunicándote a "
    "**equivalencia.fmn@gmail.com**."
)


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


def enviar_a_sheets(payload: dict) -> bool:
    url = st.secrets.get("APPS_SCRIPT_URL", "").strip()
    if not url:
        st.error("Falta configurar APPS_SCRIPT_URL en Secrets.")
        return False
    try:
        resp = requests.post(url, json=payload, timeout=15, allow_redirects=True)
        if resp.status_code == 200:
            try:
                data = resp.json()
                if data.get("status") == "ok":
                    return True
                st.error(f"Error en Apps Script: {data.get('message')}")
                return False
            except ValueError:
                st.error("Respuesta inválida del servidor. Verificá los permisos de la Web App.")
                return False
        st.error(f"Error HTTP {resp.status_code} al conectar con la planilla.")
        return False
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return False


st.title("📝 Registro de Inscripciones — Inglés 2027")
st.write("Respondé las siguientes preguntas para completar tu registro en la asignatura.")

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
    apellido_tfa = st.text_input("Apellido", key="apellido_tfa")
    nombre_tfa = st.text_input("Nombre", key="nombre_tfa")
    dni_tfa = st.text_input("DNI sin puntos (opcional)", key="dni_tfa")
    email_tfa = st.text_input("Correo electrónico (opcional)", key="email_tfa")
    carrera_tfa = st.selectbox("Seleccioná tu carrera", ["Seleccionar..."] + CARRERAS, key="carrera_tfa")

    if carrera_tfa != "Seleccionar...":
        st.warning(
            "📌 **Aviso importante:** Mientras estés cursando el **TFA**, no podés inscribirte "
            "ni cursar Inglés.\n\n"
            "1. **Antes de salir, hacé clic en el botón «Registrar mi consulta»** que figura aquí abajo "
            "para dejar asentada tu situación.\n"
            "2. Una vez que apruebes el TFA, escribinos a **inglesfmn@gmail.com** con el asunto "
            "**`aprobé el TFA`** para coordinar cómo continuar. ¡Muchos éxitos!"
        )

        if st.button("Registrar mi consulta", type="primary"):
            if not (apellido_tfa.strip() and nombre_tfa.strip()):
                st.warning("Por favor, completá Apellido y Nombre antes de registrar tu consulta.")
            else:
                with st.spinner("Registrando..."):
                    ok = enviar_a_sheets({
                        "pestana": "TFA",
                        "apellido": apellido_tfa.strip(),
                        "nombre": nombre_tfa.strip(),
                        "dni": dni_tfa.strip(),
                        "email": email_tfa.strip(),
                        "carrera": carrera_tfa,
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
            st.subheader("3. Datos personales y académicos")
            apellido = st.text_input("Apellido", key="apellido_no_tfa")
            nombre = st.text_input("Nombre", key="nombre_no_tfa")
            dni = st.text_input("DNI (sin puntos)", key="dni_no_tfa")
            email = st.text_input("Correo electrónico", key="email_no_tfa")
            carrera = st.
