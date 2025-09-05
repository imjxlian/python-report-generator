var quill = new Quill("#editor", {
    theme: "snow",
    modules: {
        syntax: false, // Syntax highlighting
        toolbar: {
            container: [
                [{ header: [1, 2, 3, 4, 5, 6, false] }], // False for normal text
                ["bold", "italic"],
                ["code-block", "inline-code"],
                ["image", "link", "blockquote"],
                [{ color: [] }, { background: [] }],
                ["clean"],
            ],
            handlers: {
                "inline-code": function () {
                    const range = quill.getSelection();
                    if (!range) return;
                    const formats = quill.getFormat(range);
                    quill.format("code", !formats.code);
                },
            },
        },
    },
});

// Handle the convert button click
document.getElementById("convertBtn").addEventListener("click", async (e) => {
    e.preventDefault(); // Prevent form submission

    const fileInput = document.getElementById("data");
    if (!fileInput.files.length) {
        alert("Please select a Markdown file.");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    const res = await fetch("/import_markdown", {
        method: "POST",
        body: formData,
    });
    const data = await res.json();

    quill.setContents([]); // vide l'éditeur avant l'insertion

    quill.clipboard.dangerouslyPasteHTML(data.html_output);

    // Set auto as default language for all code blocks
    document.querySelectorAll(".ql-code-block").forEach((block) => {
        if (!block.dataset.language || block.dataset.language === "plain") {
            block.dataset.language = "auto";
        }
    });
});

// Export PDF
document.getElementById("exportPdfBtn").addEventListener("click", () => {
    const htmlContent = quill.root.innerHTML;

    // Envoi au serveur
    fetch("/export_pdf", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ html: htmlContent }),
    })
        .then((res) => res.blob())
        .then((blob) => {
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "report.pdf";
            a.click();
            URL.revokeObjectURL(url);
        })
        .catch((err) => console.error("PDF export error:", err));
});

// Add a listener for debugging, to see the content of the editor
quill.on(Quill.events.TEXT_CHANGE, () => {
    console.log(quill.root.innerHTML);
});

const selector = document.getElementById("blockLanguageSelector");
const allowedLangs = [
    "auto",
    "solidity",
    "javascript",
    "python",
    "plain",
    "html",
    "css",
    "sql",
];
let activeContainer = null;

// When a code block is clicked
quill.root.addEventListener("click", (e) => {
    const block = e.target.closest(".ql-code-block");
    if (!block) {
        selector.style.display = "none";
        activeContainer = null;
        return;
    }

    const container = block.closest(".ql-code-block-container");
    if (!container) return;

    activeContainer = container;

    // Position the selector above the container
    const rect = container.getBoundingClientRect();
    selector.style.top = `${rect.top + window.scrollY - 30}px`;
    selector.style.right = `${rect.left + window.scrollX}px`;
    selector.style.display = "block";

    // Set the selector value to the language of the first block
    selector.value =
        container.querySelector(".ql-code-block").dataset.language || "auto";
});

// When the language is changed
selector.addEventListener("change", () => {
    if (!activeContainer) return;

    const lang = selector.value;
    if (!allowedLangs.includes(lang)) return;

    activeContainer.querySelectorAll(".ql-code-block").forEach((block) => {
        block.dataset.language = lang;
    });
});

// Inline code button
const toolbar = quill.getModule("toolbar");

const buttons = document.querySelectorAll(".ql-inline-code");
buttons.forEach((btn) => {
    btn.innerHTML = "⌨️";
});
