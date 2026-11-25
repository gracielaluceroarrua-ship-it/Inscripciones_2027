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
    "Tecnicatura Universitaria en Minería (Plan 6/15 - Vocacional)",
    "Tecnicatura Universitaria en Obras Viales (Plan 01/18 - Vocacional)",
    "Tecnicatura Universitaria en Fotografía (Plan 15/15 - Vocacional)",
]


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
    nombre_tfa = st.text_input("Apellido y Nombre completos (opcional)", key="nombre_tfa")
    dni_tfa = st.text_input("DNI sin puntos (opcional)", key="dni_tfa")
    email_tfa = st.text_input("Correo electrónico (opcional)", key="email_tfa")
    carrera_tfa = st.selectbox("Seleccioná tu carrera", ["Seleccionar..."] + CARRERAS, key="carrera_tfa")

    if carrera_tfa != "Seleccionar...":
        st.warning(
            "📌 **Aviso importante:** Mientras estés cursando el **TFA**, no podés inscribirte "
            "ni cursar Inglés. Cuando apruebes el TFA, escribinos a **inglesfmn@gmail.com** "
            "con el asunto **`aprobé el TFA`** para coordinar cómo continuar. ¡Muchos éxitos!"
        )

        if st.button("Registrar mi consulta", type="primary"):
            with st.spinner("Registrando..."):
                ok = enviar_a_sheets({
                    "pestana": "TFA",
                    "nombre": nombre_tfa.strip(),
                    "dni": dni_tfa.strip(),
                    "email": email_tfa.strip(),
                    "carrera": carrera_tfa,
                })
                if ok:
                    st.success("✅ Registro guardado. Recordá escribirnos cuando apruebes el TFA.")

# ------------------------------------------------------------------------------
# RAMA B: NO ESTÁ EN TFA (No)
# ------------------------------------------------------------------------------
elif en_tfa == "No":
    st.subheader("2. Antecedentes en el idioma")
    tiene_certificado = st.radio(
        "¿Poseés certificado internacional vigente o Inglés aprobado en otra carrera?",
        [
            "Seleccionar...",
            "Sí",
            "No",
            "No, pero poseo conocimientos sólidos de inglés",
        ],
    )

    if tiene_certificado != "Seleccionar...":
        st.subheader("3. Datos personales y académicos")
        nombre = st.text_input("Apellido y Nombre completos", key="nombre_no_tfa")
        dni = st.text_input("DNI (sin puntos)", key="dni_no_tfa")
        email = st.text_input("Correo electrónico", key="email_no_tfa")
        carrera = st.selectbox("Seleccioná tu carrera", ["Seleccionar..."] + CARRERAS, key="carrera_no_tfa")

        if tiene_certificado == "Sí":
            pestana_destino = "Con_Certificado"
            mensaje_exito = (
                "✅ **Datos registrados correctamente.**\n\n"
                "El equipo docente revisará tu situación y **se contactará con vos a la brevedad** "
                "para indicarte cómo proceder con la acreditación o equivalencia."
            )
        elif tiene_certificado == "No":
            pestana_destino = "Inscripcion_Regular"
            mensaje_exito = (
                "✅ **¡Preinscripción registrada correctamente para Inglés 2027!**"
            )
        else:
            pestana_destino = "Conocimientos_Solidos"
            mensaje_exito = (
                "✅ **Datos registrados correctamente.**\n\n"
                "El equipo docente **se contactará con vos a la brevedad** para evaluar tu situación "
                "y determinar cómo seguir."
            )

        if st.button("Enviar registro", type="primary"):
            if not (nombre.strip() and dni.strip() and email.strip()) or carrera == "Seleccionar...":
                st.warning(
                    "Por favor, completá Apellido y Nombre, DNI (sin puntos), Correo electrónico "
                    "y Carrera antes de enviar."
                )
            else:
                with st.spinner("Guardando registro..."):
                    ok = enviar_a_sheets({
                        "pestana": pestana_destino,
                        "nombre": nombre.strip(),
                        "dni": dni.strip(),
                        "email": email.strip(),
                        "carrera": carrera,
                    })
                    if ok:
                        st.success(mensaje_exito)
