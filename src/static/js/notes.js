function handleFiles(files, folderId) {
  for (const file of files) {
    const reader = new FileReader();
    reader.readAsArrayBuffer(file);
    reader.onload = () => {
      const title = file.name;
      const data = new Uint8Array(reader.result);
      createNote(title, data, folderId);
    };
  }
}


function createNote(title, data, folderId) {
  const blob = new Blob([data], { type: 'application/octet-stream' });
  const formData = new FormData();
  formData.append('title', title);
  formData.append('data', blob);
  formData.append('folder_id', folderId);

  fetch('/notes', {
    method: 'POST',
    body: formData
  }).then(response => response.json())
    .then(data => {
      if (data.success) {
        location.reload();
      }
    });
}


function createFolder() {
    // Prompt the user to enter the title of the new folder
    let folderTitle = prompt("Please enter the title of the new folder:");

    fetch('/folders', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ title: folderTitle })
    }).then(response => response.json())
    .then(data => {
        if (data.success) {
        location.reload();
        }
    });
}


function toggleNoteContent(element, noteId) {
  const noteContent = element.nextElementSibling;
  console.log('test: ', noteContent.style.display)
  if (noteContent.style.display === 'none') {
    const formData = new FormData();
    formData.append('note_id', noteId);
    fetch('/open-note', {
      method: 'POST',
      body: formData
    })
      .then(response => response.text())
      .then(data => {
        noteContent.textContent = data;
        noteContent.style.display = 'block';
      });
  } else {
    noteContent.style.display = 'none';
  }
}


function deleteNote(noteId) {
  fetch('/delete-note', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ noteId })
  }).then(response => response.json())
    .then(data => {
      if (data.success) {
        location.reload();
      }
    });
}


function deleteFolder(folderId) {
  fetch('/delete-folder', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ folderId })
  }).then(response => response.json())
    .then(data => {
      if (data.success) {
        location.reload();
      }
    });
}
