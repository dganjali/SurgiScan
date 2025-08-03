import React, { useRef } from 'react'
import './App.css'

function App() {
  const videoRef = useRef(null)

  // Static list of tool images - we'll need to copy these to public folder
  const toolImages = [
    '/tools/Cannula Tubing.png',
    '/tools/DeBakey Atraumatic Vascular Clamp:Forceps.png',
    '/tools/Finochietto-style chest retractor.png',
    '/tools/Laparotomy Sponge.png',
    '/tools/Needle Counter.png',
    '/tools/Needle holders.png',
    '/tools/Scalpel Blades.png',
    '/tools/Sterile Suture Packs.png',
    '/tools/Surgical towels.png',
    '/tools/Surgical Vessel Tubes.png',
    '/tools/Syringe Pail.png',
    '/tools/Thoracic Rib elevator.png'
  ]

  const handleVideoError = (e) => {
    console.error('Video error:', e)
    console.error('Video error details:', e.target.error)
  }

  const handleVideoLoad = () => {
    console.log('Video loaded successfully')
  }

  return (
    <div className="app">
      <header className="header">
        <h1>Surgical Tools Viewer</h1>
      </header>
      
      <main className="main-content">
        <div className="video-section">
          <h2>Output Video</h2>
          <video 
            ref={videoRef}
            controls 
            width="100%" 
            height="auto"
            className="video-player"
            onError={handleVideoError}
            onLoadedData={handleVideoLoad}
            preload="metadata"
          >
            <source src="/output.mp4" type="video/mp4" />
            Your browser does not support the video tag.
          </video>
          <p style={{ marginTop: '10px', fontSize: '14px', color: '#666' }}>
            Video source: /output.mp4
          </p>
        </div>
        
        <div className="tools-section">
          <h2>Surgical Tools</h2>
          <div className="tools-grid">
            {toolImages.map((image, index) => (
              <div key={index} className="tool-item">
                <img 
                  src={image} 
                  alt={`Surgical tool ${index + 1}`}
                  className="tool-image"
                  onError={(e) => {
                    e.target.style.display = 'none'
                    e.target.nextSibling.textContent = 'Image not found'
                  }}
                />
                <p className="tool-name">
                  {image.split('/').pop().replace('.png', '').replace(/([A-Z])/g, ' $1').trim()}
                </p>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  )
}

export default App 