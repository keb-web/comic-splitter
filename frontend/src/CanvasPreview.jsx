// we need to get imagees and draw depending info from template
// need to see if dran things on canvas can be resized and how to dynamically
// update template when it is resized

// this is done already with react-konva just implement it!
// fix sizing image issues
// 	 full pages are being rendered based on panel sizes
// 	 if etched we just need to display the image without specifying
// 	 affix div size and do not let updates values change it

// add rectangles based on templates
// drawn rectangles need to be cleared if form is reset or next page button is pressed

import { useEffect, useMemo, useState} from 'react';
import { Stage, Layer, Rect, Image} from 'react-konva';
import useImage from 'use-image'


// This Canvas Preview should only work with etched
// on crop, it should just be a simple carosel
function CanvasPreview({splitTemplate, splitImages, className, galleryHeight, galleryWidth}){
	const [pageIndex, setPageIndex] = useState(0)
	const [imgWidth, setImgWidth] = useState(0)
	const [imgHeight, setImgHeight] = useState(0)
	const [offsetX, setOffsetX] = useState(0)
	const [offsetY, setOffsetY] = useState(0)
	const [scale, setScale] = useState(0)

	let pageTemplate = {}
	if (splitTemplate.pages){
		pageTemplate = splitTemplate.pages[pageIndex].panels
	}

	const filetype = splitTemplate.filetype
	const splitImageURLS = useMemo(() => {
		if (!splitImages) return [];
		function base64ToImageUrl(base64) {
			const binary = atob(base64);
			const len = binary.length;
			const bytes = new Uint8Array(len);
			for (let i = 0; i < len; i++) bytes[i] = binary.charCodeAt(i);
			const blob = new Blob([bytes], { type: filetype });
			return URL.createObjectURL(blob);
		};
		return splitImages.map(bytes => base64ToImageUrl(bytes));
	}, [splitImages, filetype]);

	useEffect(() => {
	  return () => splitImageURLS.forEach((url) => URL.revokeObjectURL(url));
	}, [splitImageURLS]);

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

	function PanelRectList({pageTemplate}) {

	  console.log('template', pageTemplate)
	  if (!pageTemplate) { return <></> }
	  return (
		<Layer className='canvasLayer' >
		  {pageTemplate.map((panelTemplate, index) => {
			const panelX = panelTemplate.x * scale + offsetX;
			const panelY = panelTemplate.y * scale + offsetY;
			const panelWidth = panelTemplate.width * scale;
			const panelHeight = panelTemplate.height * scale;

			return (
			  <Rect
				key={index}
				x={panelX}
				y={panelY}
				width={panelWidth}
				height={panelHeight}
			  />
			);
		  })}
		</Layer>
	  );
	}
	
	return (
		<div className={className}>
			<Stage width={galleryWidth} height={galleryHeight}>

				<Layer className='bgLayer'>
					<URLImage src={splitImageURLS[pageIndex]} galleryWidth={galleryWidth} galleryHeight={galleryHeight}/>
				</Layer>
				<PanelRectList pageTemplate={pageTemplate}/>
			</Stage>
		</div>
	)
}

export default CanvasPreview
