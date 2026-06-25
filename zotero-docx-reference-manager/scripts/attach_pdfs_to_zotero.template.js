// Run inside Zotero: Tools -> Developer -> Run JavaScript.
// Replace ATTACHMENTS with entries of:
// [zoteroItemKey, absolutePdfPath, attachmentTitle]

const ATTACHMENTS = [
  // ["ITEMKEY", "/absolute/path/to/paper.pdf", "Paper title"],
];

const libraryID = Zotero.Libraries.userLibraryID;
const results = [];

async function importPdf(file, parentItemID, title) {
  try {
    return await Zotero.Attachments.importFromFile({
      file,
      parentItemID,
      title,
      contentType: "application/pdf",
    });
  } catch (err) {
    if (!Zotero.File || !Zotero.File.pathToFile) {
      throw err;
    }
    return await Zotero.Attachments.importFromFile({
      file: Zotero.File.pathToFile(file),
      parentItemID,
      title,
      contentType: "application/pdf",
    });
  }
}

for (const [key, file, title] of ATTACHMENTS) {
  const parent = Zotero.Items.getByLibraryAndKey(libraryID, key);
  if (!parent) {
    results.push(`MISSING ITEM ${key}: ${title}`);
    continue;
  }

  const duplicate = parent
    .getAttachments()
    .map(id => Zotero.Items.get(id))
    .some(att => att && att.attachmentContentType === "application/pdf" && att.getField("title") === title);

  if (duplicate) {
    results.push(`SKIP EXISTING ${key}: ${title}`);
    continue;
  }

  try {
    await importPdf(file, parent.id, title);
    results.push(`ATTACHED ${key}: ${title}`);
  } catch (err) {
    results.push(`ERROR ${key}: ${title} :: ${err.message || err}`);
  }
}

return results.join("\n");
