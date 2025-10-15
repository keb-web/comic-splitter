import { useEffect, useRef, useState } from 'react'

import ImagePreview from './ImagePreview'
import ImageSubmit from './ImageSubmit'
import './App.css'
import CanvasPreview from './CanvasPreview'

function App() {
	const [splitImages, setSplitImages] = useState([])
	const [splitTemplate, setSplitTemplate] = useState([])
	const [splitData, setSplitData] = useState([])

	const imageGalleryRef = useRef(null)
	const [galleryWidth, setGalleryWidth] = useState(0);
	const [galleryHeight, setGalleryHeight] = useState(0);

	useEffect(() => {
		if (!imageGalleryRef.current) return;
		const resizeObserver = new ResizeObserver(entries => {
		  for (let entry of entries) {
			setGalleryWidth(entry.contentRect.width);
			setGalleryHeight(entry.contentRect.height);
		  }
		});
		resizeObserver.observe(imageGalleryRef.current)
		return () => {
			resizeObserver.disconnect()
		}
	}, []);


	return (
		<div className='app'>
			<div className='header'>
				<h1>comic splitter</h1>
			</div>

			<div className='options'>
				<ImageSubmit setSplitImages={setSplitImages} setSplitTemplate={setSplitTemplate} setSplitData={setSplitData}/>
				<button className='zip'>download as .zip</button>
			</div>

			<div className='imageGallery' ref={imageGalleryRef}>
				<CanvasPreview className='canvasPreview' splitTemplate={splitTemplate} splitImages={splitImages} galleryHeight={galleryHeight} galleryWidth={galleryWidth} />
				<ImagePreview splitData={splitData} />
			</div>
			
		</div>
	)
}

export default App
