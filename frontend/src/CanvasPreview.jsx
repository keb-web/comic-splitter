// we need to get imagees and draw depending info from template
// need to see if dran things on canvas can be resized and how to dynamically
// update template when it is resized

// this is done already with react-konva just implement it!
// fix sizing image issues
// 	 full pages are being rendered based on panel sizes
// 	 if etched we just need to display the image without specifying
// 	 affix div size and do not let updates values change it

// add rectangles based on tempaltes
// drawn rectangles need to be cleared if form is reset or next page button is pressed

import { useEffect, useMemo, useState} from 'react';
import { Stage, Layer, Rect, Image} from 'react-konva';
import useImage from 'use-image'


// This Canvas Preview should only work with etched
// on crop, it should just be a simple carosel
function CanvasPreview({splitTemplate, splitImages, className, galleryHeight, galleryWidth}){
	const [imgWidth, setImgWidth] = useState(0)
	const [imgHeight, setImgHeight] = useState(0)
	const [offsetX, setOffsetX] = useState(0)
	const [offsetY, setOffsetY] = useState(0)
	const [scale, setScale] = useState(0)

	let panelX = 0, panelWidth = 0, panelHeight = 0, panelY = 0
	if (splitTemplate.pages){
		const testTemplate = splitTemplate.pages[0].panels[0]
		panelX = testTemplate.x
		panelWidth = testTemplate.width
		panelHeight = testTemplate.height
		panelY = testTemplate.y
	}

	const filetype = splitTemplate.filetype
	function base64ToImageUrl(base64) {
		const binary = atob(base64);
		const len = binary.length;
		const bytes = new Uint8Array(len);
		for (let i = 0; i < len; i++) bytes[i] = binary.charCodeAt(i);
		const blob = new Blob([bytes], { type: filetype });
		return URL.createObjectURL(blob);
	};
	const splitImageURLS = useMemo(() => {
		if (!splitImages) return [];
		return splitImages.map(bytes => base64ToImageUrl(bytes));
	}, [splitImages, filetype]);

	useEffect(() => {
	  return () => splitImageURLS.forEach((url) => URL.revokeObjectURL(url));
	}, [splitImageURLS]);

	let testImg = splitImageURLS[0];

	const URLImage = ({src, galleryWidth, galleryHeight, ...rest}) => {
		let [image] = useImage(src, 'anonymous')

        useEffect(() => {
          if (image) {
            const width = image.naturalWidth;
            const height = image.naturalHeight;

			const scaleX = galleryWidth / width;
			const scaleY = galleryHeight / height;
			const newScale = Math.min(scaleX, scaleY);
			const offsetX = (galleryWidth - width * newScale) / 2;
			const offsetY = (galleryHeight - height * newScale) / 2;

			setScale(newScale)
			setImgHeight(height * newScale);
			setImgWidth(width * newScale);
			setOffsetX(offsetX);
			setOffsetY(offsetY);

          }
        }, [image, galleryWidth, galleryHeight]);

		return <Image 
					image={image}
					x={offsetX}
				    y={offsetY}
		  			width={imgWidth}
					height={imgHeight}
					{...rest}
				/>
	}

	
	return (
		<div className={className}>
			<Stage width={galleryWidth} height={galleryHeight}>

				<Layer className='bgLayer'>
					<URLImage src={testImg} galleryWidth={galleryWidth} galleryHeight={galleryHeight}/>
				</Layer>

				<Layer className='canvasLayer'>
					<Rect x={panelX * scale + offsetX} width={panelWidth*scale} y={panelY * scale + offsetY} height={panelHeight * scale} stroke='yellow'></Rect>
				</Layer>

			</Stage>
		</div>
	)
}

export default CanvasPreview
