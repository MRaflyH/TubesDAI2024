import { useState, useEffect } from "react";
import { Canvas, useThree } from "@react-three/fiber";
import { OrbitControls, Text } from "@react-three/drei";
import FloatingController from "./FloatingController";
import * as THREE from "three";

const MagicCubeReplayPlayer = () => {
  const [replayData, setReplayData] = useState<number[][]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [playbackSpeed, setPlaybackSpeed] = useState(1);
  const [gap, setGap] = useState(0.1);

  useEffect(() => {
    const generatedData = Array.from({ length: 100 }, () => {
      return Array.from(
        { length: 125 },
        () => Math.floor(Math.random() * 125) + 1
      );
    });
    setReplayData(generatedData);
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
    <div className="relative w-full min-h-screen bg-gray-900 overflow-hidden">
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
                const y =
                  Math.floor((index % 25) / 5) * (1 + gap) - 2 * (1 + gap);
                const z = Math.floor(index / 25) * (1 + gap) - 2 * (1 + gap);

                return (
                  <group key={index} position={[x, y, z]}>
                    <mesh
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
                        color={`hsl(${(value / 125) * 360}, 100%, 50%)`}
                      />
                    </mesh>
                    <Text
                      position={[0, 0, 0.51]}
                      fontSize={0.2}
                      color="#ffffff"
                    >
                      {value}
                    </Text>
                  </group>
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
