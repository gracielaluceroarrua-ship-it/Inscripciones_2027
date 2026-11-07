import datetime
import gspread
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Inscripción Académica 2026", page_icon="📝", layout="centered"
)

st.title("📝 Sistema de Inscripción Académica")

# --- ID DE LA PLANILLA DE GOOGLE SHEETS ---
SPREADSHEET_ID = "14o-xOc6WB0kqycpUPE6K7rmu3dfiV1poVbCBsZQBs5I"


# --- CONEXIÓN CON GOOGLE SHEETS ---
@st.cache_resource
def conectar_google_sheets():
  try:
    gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
    sh = gc.open_by_key(SPREADSHEET_ID)
    return sh
  except Exception as e:
    return None


sh = conectar_google_sheets()

# --- INICIALIZACIÓN DE ESTADOS ---
if "paso" not in st.session_state:
  st.session_state.paso = 1
if "tfa" not in st.session_state:
  st.session_state.tfa = ""
if "certificado_opcion" not in st.session_state:
  st.session_state.certificado_opcion = ""


# ==========================================
# PASO 1: ¿Estás en TFA?
# ==========================================
if st.session_state.paso == 1:
  st.subheader("1. Estado Académico")
  tfa_respuesta = st.radio("¿Estás cursando TFA?", ["Seleccione...", "Sí", "No"])

  if st.button("Siguiente"):
    if tfa_respuesta == "Seleccione...":
      st.warning("Por favor, seleccione una opción.")
    else:
      st.session_state.tfa = tfa_respuesta
      if tfa_respuesta == "Sí":
        st.session_state.paso = 2  # Va a sección TFA
      else:
        st.session_state.paso = 3  # Va a sección de certificados
      st.rerun()


# ==========================================
# PASO 2: Camino SÍ cursa TFA
# ==========================================
elif st.session_state.paso == 2:
  st.subheader("2. Registro - Cursa TFA")

  with st.form("tfa_form"):
    carrera_tfa = st.selectbox(
        "Seleccione su carrera:",
        [
            "Seleccione...",
            "Licenciatura en Ciencias de la Computación",
            "Ingeniería en Informática",
            "Profesorado en Matemática",
            "Tecnicatura Web",
        ],
    )
    enviar_tfa = st.form_submit_button("Registrar situación")

  if enviar_tfa:
    if carrera_tfa == "Seleccione...":
      st.warning("Por favor, seleccione su carrera.")
    elif sh is None:
      st.error("Error de conexión con Google Sheets.")
    else:
      fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      try:
        hoja = sh.worksheet("TFA_Rechazados")
        fila = [fecha_hora, carrera_tfa, "Cursa TFA"]
        hoja.append_row(fila)
        st.session_state.enviado = True
      except Exception as e:
        st.error(f"Error al guardar: {e}")

  if st.session_state.get("enviado", False):
    st.error(
        "⚠️ **Aviso importante:** Actualmente no puedes cursar. Por favor,"
        " comunícate con el equipo docente cuando apruebes para coordinar cómo"
        " seguir escribiendo a **inglesfmn@gmail.com** con el asunto **'aprobé"
        " el TFA'**."
    )
    if st.button("Reiniciar"):
      st.session_state.clear()
      st.rerun()


# ==========================================
# PASO 3: Camino NO cursa TFA (Elección de Certificado)
# ==========================================
elif st.session_state.paso == 3:
  st.subheader("2. Acreditación de Idioma")
  cert_opcion = st.radio(
      "¿Posee certificado de inglés?",
      [
          "Seleccione...",
          "Sí",
          "No",
          "No, pero poseo conocimientos sólidos de inglés",
      ],
  )

  col1, col2 = st.columns(2)
  with col1:
    if st.button("Volver"):
      st.session_state.paso = 1
      st.rerun()
  with col2:
    if st.button("Continuar"):
      if cert_opcion == "Seleccione...":
        st.warning("Por favor, seleccione una opción.")
      else:
        st.session_state.certificado_opcion = cert_opcion
        st.session_state.paso = 4
        st.rerun()


# ==========================================
# PASO 4: Formulario de Datos Personales + Subida de Certificado (si corresponde)
# ==========================================
elif st.session_state.paso == 4:
  opcion = st.session_state.certificado_opcion

  if opcion == "Sí":
    st.subheader("3. Complete sus datos y adjunte su certificado de inglés")
    pestana_destino = "Inscriptos_Con_Certificado"
  elif opcion == "No":
    st.subheader("3. Complete sus datos (Inscriptos sin certificado)")
    pestana_destino = "Inscriptos_Sin_Certificado"
  else:
    st.subheader(
        "3. Complete sus datos (Conocimientos sólidos sin certificado)"
    )
    pestana_destino = "Conocimientos_Solidos"

  with st.form("datos_form"):
    nombre_apellido = st.text_input("Nombre y apellido completos")
    dni = st.text_input("DNI (sin puntos)")
    carrera = st.selectbox(
        "Seleccione su carrera:",
        [
            "Seleccione...",
            "Licenciatura en Ciencias de la Computación",
            "Ingeniería en Informática",
            "Profesorado en Matemática",
            "Tecnicatura Web",
        ],
    )

    archivo_certificado = None
    if opcion == "Sí":
      archivo_certificado = st.file_uploader(
          "Adjuntar certificado de inglés (PDF o Imagen)",
          type=["pdf", "png", "jpg", "jpeg"],
      )

    enviar_datos = st.form_submit_button("Finalizar inscripción")

  if enviar_datos:
    if not nombre_apellido or not dni or carrera == "Seleccione...":
      st.warning("Por favor, complete todos los campos obligatorios.")
    elif opcion == "Sí" and archivo_certificado is None:
      st.warning("Por favor, adjunte su certificado de inglés antes de enviar.")
    elif sh is None:
      st.error("Error de conexión con Google Sheets.")
    else:
      fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      dni_limpio = "".join(filter(str.isdigit, str(dni)))

      nombre_archivo = (
          archivo_certificado.name if archivo_certificado else "N/A"
      )

      try:
        hoja = sh.worksheet(pestana_destino)
        fila = [
            fecha_hora,
            nombre_apellido,
            dni_limpio,
            carrera,
            opcion,
            nombre_archivo,
        ]
        hoja.append_row(fila)
        st.session_state.registro_exitoso = True
      except Exception as e:
        st.error(f"Error al registrar los datos en la planilla: {e}")

  if st.session_state.get("registro_exitoso", False):
    st.success("¡Información registrada correctamente!")

    if opcion == "Sí":
      st.info(
          "📩 **¡Gracias!** Serás contactado a la brevedad por el equipo"
          " docente para determinar cómo seguir."
      )
    elif opcion == "No":
      st.info(
          "✅ **¡Inscripción registrada con éxito!** Tus datos se guardaron"
          " correctamente en el sistema."
      )
    else:
      st.info(
          "📩 **¡Gracias!** Serás contactado por el equipo docente para"
          " determinar cómo seguir."
      )

    if st.button("Hacer otra consulta"):
      st.session_state.clear()
      st.rerun()
