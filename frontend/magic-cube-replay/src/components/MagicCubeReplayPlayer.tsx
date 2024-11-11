import { useState, useEffect, useMemo } from "react";
import { Canvas, useThree } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import FloatingController from "./FloatingController";
import * as THREE from "three";
import axios from "axios";

// Function to create canvas texture with a given number
const createNumberTexture = (number: number) => {
  const size = 256;
  const canvas = document.createElement("canvas");
  canvas.width = size;
  canvas.height = size;
  const context = canvas.getContext("2d");
  if (context) {
    // Set background color (optional)
    context.fillStyle = "black";
    context.fillRect(0, 0, size, size);
    // Set text properties
    context.fillStyle = "white";
    context.font = `${size / 2}px Arial`;
    context.textAlign = "center";
    context.textBaseline = "middle";
    context.fillText(number.toString(), size / 2, size / 2);
  }
  return new THREE.CanvasTexture(canvas);
};

const MagicCubeReplayPlayer = () => {
  const [replayData, setReplayData] = useState<number[][]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [playbackSpeed, setPlaybackSpeed] = useState(1);
  const [gap, setGap] = useState(0.1);

  // Pre-render all textures for numbers 1 to 125
  const textures = useMemo(() => {
    const generatedTextures = [];
    for (let i = 1; i <= 125; i++) {
      generatedTextures.push(createNumberTexture(i));
    }
    return generatedTextures;
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const generatedData = Array.from({ length: 100 }, () =>
          Array.from({ length: 125 }, () => Math.floor(Math.random() * 125) + 1)
        );
        setReplayData(generatedData);

        const response = await axios.post("http://127.0.0.1:8001/run-algorithm/", {
          initial_cube: Array(125).fill(1),
          objective_function: "var",
          value_objective: 0,
          max_iterations: 100,
          algorithm: "steepest_ascent",
        });
        setReplayData(response.data.replayData || generatedData);
      } catch (error) {
        console.error("Error fetching initial replay data:", error);
      }
    };

    fetchData();
  }, []);

  useEffect(() => {
    if (isPlaying) {
      const interval = setInterval(() => {
        setCurrentIndex((prevIndex) => {
          if (prevIndex < replayData.length - 1) {
            return prevIndex + 1;
          } else {
            clearInterval(interval);
            setIsPlaying(false);
            return prevIndex;
          }
        });
      }, 1000 / playbackSpeed);

      return () => clearInterval(interval);
    }
  }, [isPlaying, playbackSpeed, replayData]);

  const handlePlayPause = () => {
    setIsPlaying(!isPlaying);
  };

  const handleSpeedChange = (value: number) => {
    setPlaybackSpeed(value);
  };

  const handleProgressChange = (value: number) => {
    setCurrentIndex(value);
    if (value === replayData.length - 1) {
      setIsPlaying(false);
    }
  };

  const handleReset = () => {
    setCurrentIndex(0);
    setIsPlaying(false);
  };

  const handleGapChange = (value: number) => {
    setGap(value);
  };

  return (
    <div className="relative w-full min-h-screen bg-slate-600 overflow-hidden">
      <div className="flex justify-center items-center w-full h-screen overflow-hidden">
        <Canvas
          className="h-full w-full"
          camera={{ position: [10, 10, 10], fov: 40 }}
        >
          <ZoomOrbitControls gap={gap} />
          <ambientLight intensity={0.5} />
          <pointLight position={[10, 10, 10]} />

          {replayData.length > 0 && replayData[currentIndex] && (
            <group>
              {replayData[currentIndex].map((value, index) => {
                const x = (index % 5) * (1 + gap) - 2 * (1 + gap);
                const y = Math.floor((index % 25) / 5) * (1 + gap) - 2 * (1 + gap);
                const z = Math.floor(index / 25) * (1 + gap) - 2 * (1 + gap);

                return (
                  <mesh
                    key={index}
                    position={[x, y, z]}
                    onPointerOver={(e) => {
                      e.stopPropagation();
                      document.body.style.cursor = "pointer";
                    }}
                    onPointerOut={() => {
                      document.body.style.cursor = "default";
                    }}
                  >
                    <boxGeometry args={[0.9, 0.9, 0.9]} />
                    <meshStandardMaterial
                      map={textures[value - 1]} // Apply unique texture for each cube
                    />
                  </mesh>
                );
              })}
            </group>
          )}
        </Canvas>
      </div>

      {replayData.length > 0 && (
        <div className="absolute bottom-12 left-1/2 transform -translate-x-1/2 z-10 cursor-grab">
          <FloatingController
            isPlaying={isPlaying}
            currentIndex={currentIndex}
            replayData={replayData}
            setReplayData={setReplayData}
            playbackSpeed={playbackSpeed}
            handlePlayPause={handlePlayPause}
            handleProgressChange={handleProgressChange}
            handleSpeedChange={handleSpeedChange}
            handleReset={handleReset}
            gap={gap}
            handleGapChange={handleGapChange}
            initialGap={0.1}
          />
        </div>
      )}
    </div>
  );
};

// Custom Zoom and Pan Control Component
function ZoomOrbitControls({ gap }: { gap: number }) {
  const { camera, gl, mouse } = useThree();

  useEffect(() => {
    const handleWheel = (event: WheelEvent) => {
      if (gap === 10) {
        const zoomFactor = event.deltaY * 0.002;
        const vector = new THREE.Vector3(mouse.x, mouse.y, 0.5).unproject(
          camera
        );
        const direction = vector.sub(camera.position).normalize();
        camera.position.addScaledVector(direction, zoomFactor);
        camera.updateProjectionMatrix();
      }
    };

    gl.domElement.addEventListener("wheel", handleWheel);

    return () => {
      gl.domElement.removeEventListener("wheel", handleWheel);
    };
  }, [camera, gl, mouse, gap]);

  return (
    <OrbitControls
      target={[0, 0, 0]}
      enableZoom={true}
      enablePan={true}
      maxDistance={50}
      mouseButtons={{
        LEFT: THREE.MOUSE.ROTATE,
        MIDDLE: THREE.MOUSE.PAN,
      }}
    />
  );
}

export default MagicCubeReplayPlayer;
