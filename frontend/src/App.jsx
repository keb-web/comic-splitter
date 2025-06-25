// import { useState } from 'react'
import './App.css'

function SubmitImage() {
	function handleSubmit(e) {
		e.preventDefault();
		const form = e.target;
		const formData = new FormData(form);

		// TODO: ensure that datatype is correct
		
		// pass into api
		// fetch('/some-api', { method: form.method, body: formData });

		const formJson = Object.fromEntries(formData.entries());

		// for (var pair of formData.entries()) {
		// 	console.log(pair[0] + ', ' + pair[1].name);
		// }

		console.log('formJson', formJson)
	}
	return (
		<form method='post' onSubmit={handleSubmit}>
			<input name='comic' type='file' accept='image/png, image/jpeg' multiple/>
			<button type="reset">Reset form</button>
			<button type="submit">Submit form</button>
			<hr/>
		</form>
	);
}

function App() {
	return (
		<>
			<h1>comic splitter</h1>
			<p>only png and jpeg supported currently</p>
			<SubmitImage />
		</>
	)
}

export default App
