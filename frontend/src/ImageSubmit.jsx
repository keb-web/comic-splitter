import { useState } from 'react'

function ImageSubmit({ setSplitImages, setSplitTemplate, setSplitData }) {
	const [label, setLabel] = useState(false)
	const [blank, setBlank] = useState(false)
	const [margins, setMargins] = useState(0)
	const [mode, setMode] = useState('crop')
	const [author, setAuthor] = useState('author')
	const [title, setTitle] = useState('title')
	const [entryNumber, setEntryNumber] = useState(0)
	const valid_filetypes = ['image/jpeg', 'image/png', 'image/jpg']

	function handleSubmit(e) {
		e.preventDefault();
		const form = e.target;
		const formData = new FormData(form);
		if (!_valid_file_extension(formData)) {
			return
		}

		formData.append("label", label);
		formData.append("blank", blank);
		formData.append("margins", margins);
		formData.append("mode", mode);

		formData.append("author", author);
		formData.append("title", title);
		formData.append("entryNumber", entryNumber);

		retrieveSplitImages(formData, form)
	}

	function _valid_file_extension(formData) {
		const file = formData.get('files')
		if (valid_filetypes.includes(file.type) == false) {
			console.error('Invalid File Type')
			return false
		}
		return true
	}

	async function retrieveSplitImages(formData, form) {
		const some_endpoint = 'http://127.0.0.1:8000/split'
		try {
			const response = await fetch(some_endpoint, {
				method: form.method,
				body: formData,
			});
			if (!response.ok) {
				throw new Error('Response status: ${response.status}');
			}
			const splitData = await response.json()
			const template = splitData.template
			const images = splitData.images
			setSplitData(splitData)
			setSplitTemplate(template)
			setSplitImages(images)

		} catch (error) {
			console.error(error)
		}
	}

	return (
		<form className='inputForm' method='post' onSubmit={handleSubmit}>
			<p>Upload (png & jpeg)</p>
			<input name='files' type='file' accept='image/png, image/jpeg, image/jpg' multiple />
			<button type="reset" onClick={() => { setSplitImages([]) }}>Reset form</button>
			<button type="submit">Submit form</button>
			<hr/>
			<div className='optionsFormContainer'>
				<p>Options</p>
				<label>
					<input type="radio" name="mode" value="crop" checked={mode == 'crop'} onChange={() => setMode('crop')}/>
					Crop
				</label>
				<label>
					<input type="radio" name="mode" value="etch" checked={mode == 'etch'} onChange={() => setMode('etch')}/>
					Etch
				</label>
				<label>
					<input type="checkbox" id="label" name="label" value="label" checked={label} onChange={(e) => setLabel(e.target.checked)}/>
					Label
				</label>
				<label>
					<input type="checkbox" id="blank" name="blank" value="blank" checked={blank} onChange={(e) => setBlank(e.target.checked)}/>
					Blank
				</label>
				<label>
					Margins
					<input type="number" id="margins" name="margins" min='0' max='25' value={margins} onChange={(e) => setMargins(e.target.value)}/>
				</label>
			</div>
			<hr />
				<div className='metadataFormContainer'>
					<p>Metadata</p>
					<label>
						Author
						<input type='text' id='author' name='author' value={author} onChange={(e) => setAuthor(e.target.value)}/>
					</label>
					<label>
						Title
						<input type='text' id='title' name='title' value={title} onChange={(e) => setTitle(e.target.value)}/>
					</label>
					<label>
						entry number (optional)
						<input type='entry_number' id='entry_number' name='entry_number' value={entryNumber} onChange={(e) => setEntryNumber(e.target.value)}/>
					</label>
				</div>
			<hr />
		</form>
	);
}

export default ImageSubmit
