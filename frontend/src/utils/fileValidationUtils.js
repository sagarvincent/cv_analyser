export const ALLOWED_EXTENSIONS = ['pdf', 'docx', 'doc'];
export const MAX_FILE_SIZE_BYTES = 16 * 1024 * 1024;

// -------------------- validateFile ----------- START ----------
// -- Calls : nothing (leaf)
// -- Called by: UploadScreen
export function validateFile(file) {
  const ext = file.name.includes('.') ? file.name.split('.').pop().toLowerCase() : '';
  if (!ALLOWED_EXTENSIONS.includes(ext)) {
    const allowed = ALLOWED_EXTENSIONS.map((e) => e.toUpperCase()).join(', ');
    return `'.${ext || '?'}' files are not supported. Upload a ${allowed} file.`;
  }
  if (file.size > MAX_FILE_SIZE_BYTES) {
    return `File is ${(file.size / 1024 / 1024).toFixed(1)} MB — exceeds the 16 MB limit.`;
  }
  return null;
}
// -------------------- validateFile ------------- END ----------------
