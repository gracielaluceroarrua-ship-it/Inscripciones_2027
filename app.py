function doPost(e) {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const data = JSON.parse(e.postData.contents);

    const nombrePestana = data.pestana || "Inscripcion_Regular";
    const sheet = ss.getSheetByName(nombrePestana);

    if (!sheet) {
      return ContentService
        .createTextOutput(JSON.stringify({
          status: "error",
          message: "No se encontró la pestaña: " + nombrePestana
        }))
        .setMimeType(ContentService.MimeType.JSON);
    }

    sheet.appendRow([
      new Date(),
      data.nombre || "",
      data.dni || "",
      data.email || "",
      data.carrera || ""
    ]);

    return ContentService
      .createTextOutput(JSON.stringify({ status: "ok" }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: "error", message: err.message }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}
