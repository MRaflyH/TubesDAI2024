import { useState, useEffect } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import FloatingController from "./FloatingController";

const MagicCubeReplayPlayer = () => {
  const [replayData, setReplayData] = useState<number[][]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [playbackSpeed, setPlaybackSpeed] = useState(1);
  const [playbackInterval, setPlaybackInterval] =
    useState<ReturnType<typeof setTimeout> | null>(null);

  // Mock data to simulate replay data for each iteration
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
      setPlaybackInterval(interval);

      return () => clearInterval(interval);
    } else {
      if (playbackInterval) {
        clearInterval(playbackInterval);
        setPlaybackInterval(null);
      }
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
  };

  // Define handleReset function
  const handleReset = () => {
    setCurrentIndex(0);
    setIsPlaying(false);
  };

  return (
    <div className="relative w-full min-h-screen bg-gray-900 overflow-hidden">
      <div className="flex justify-center items-center w-full h-screen overflow-hidden">
        <Canvas
          className="h-full w-full"
          camera={{ position: [0, 0, 10], fov: 75 }}
        >
          <OrbitControls enableZoom={true} maxDistance={20} minDistance={6} />
          <ambientLight intensity={0.5} />
          <pointLight position={[10, 10, 10]} />
          {replayData.length > 0 && replayData[currentIndex] && (
            <group>
              {replayData[currentIndex].map((value, index) => {
                const x = (index % 5) - 2;
                const y = Math.floor((index % 25) / 5) - 2;
                const z = Math.floor(index / 25) - 2;
                return (
                  <mesh
                    key={index}
                    position={[x, y, z]}
                    onPointerOver={(e) => {
                      e.stopPropagation();
                      document.body.style.cursor = "grab";
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
            handleReset={handleReset} // Pass handleReset here
          />
        </div>
      )}
    </div>
  );
};

export default MagicCubeReplayPlayer;
