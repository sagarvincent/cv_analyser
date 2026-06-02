ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}
MAX_FILE_SIZE_BYTES = 16 * 1024 * 1024  # 16 MB


class FileValidator:
    # -------------------- validate ----------- START ----------
    # -- Calls : nothing (leaf)
    # -- Called by: validate_upload (interface.py)
    def validate(self, filename: str, size_bytes: int) -> tuple[bool, str | None]:
        ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        if ext not in ALLOWED_EXTENSIONS:
            allowed = ", ".join(ext.upper() for ext in sorted(ALLOWED_EXTENSIONS))
            return False, f"'.{ext or '?'}' files are not supported. Upload a {allowed} file."
        if size_bytes > MAX_FILE_SIZE_BYTES:
            mb = size_bytes / 1024 / 1024
            return False, f"File is {mb:.1f} MB — exceeds the 16 MB limit."
        return True, None
    # -------------------- validate ------------- END ----------------
