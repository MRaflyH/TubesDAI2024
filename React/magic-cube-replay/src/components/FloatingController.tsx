import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";
import styled from "styled-components";
import { Button, Select, Slider, Modal, Table, Typography } from "antd";
import { PlayIcon, PauseIcon, ArrowPathIcon } from "@heroicons/react/24/solid";

const { Text } = Typography;

const GlassContainer = styled(motion.div)`
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.2);
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.06);
  width: 500px; /* Increased width */
  cursor: grab;
  display: flex; /* Use flexbox for layout */
  flex-direction: column; /* Arrange elements vertically */
  align-items: center; /* Align items to center */
  padding: 20px; /* Add padding for better spacing */
  gap: 10px; /* Add gap between items */
`;

const ControlRow = styled.div`
  display: flex;
  width: 100%;
  justify-content: space-between;
  gap: 20px;
  align-items: center;
`;

const SliderWrapper = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
`;

interface FloatingControllerProps {
  isPlaying: boolean;
  currentIndex: number;
  replayData: number[][];
  playbackSpeed: number;
  handlePlayPause: () => void;
  handleProgressChange: (value: number) => void;
  handleSpeedChange: (value: number) => void;
  handleReset: () => void;
}

const FloatingController: React.FC<FloatingControllerProps> = ({
  isPlaying,
  currentIndex,
  replayData,
  playbackSpeed,
  handlePlayPause,
  handleProgressChange,
  handleSpeedChange,
  handleReset,
}) => {
  const [speed, setSpeed] = useState(playbackSpeed);
  const [selectedIteration, setSelectedIteration] = useState(currentIndex);
  const [detailVisible, setDetailVisible] = useState(false);
  const [selectedAlgorithm, setSelectedAlgorithm] = useState(
    "Steepest Ascent Hill-Climbing"
  );

  useEffect(() => {
    setSelectedIteration(currentIndex); // Sync selected iteration with currentIndex
  }, [currentIndex]);

  const handleIterationChange = (value: number) => {
    setSelectedIteration(value);
    handleProgressChange(value); // Trigger progress change
  };

  const showDetailModal = () => {
    setDetailVisible(true);
  };

  const handleDetailClose = () => {
    setDetailVisible(false);
  };

  const onSpeedChange = (value: number) => {
    setSpeed(value);
    handleSpeedChange(value);
  };

  const handleAlgorithmChange = (value: string) => {
    setSelectedAlgorithm(value);
  };

  // Prepare data for the table
  const columns = [
    {
      title: "Index",
      dataIndex: "index",
      key: "index",
    },
    {
      title: "Value",
      dataIndex: "value",
      key: "value",
    },
  ];

  const dataSource = replayData[selectedIteration].map(
    (value: number, index: number) => ({
      index: index + 1,
      value: value,
    })
  );

  return (
    <GlassContainer
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      drag
      dragConstraints={{
        left: 0,
        right: 0,
        top: 0,
        bottom: 0,
      }}
      dragElastic={0.1}
    >
      {/* Algorithm Selection */}
      <Text className="mb-2 text-white text-left w-full">
        Select Algorithm:
      </Text>
      <ControlRow>
        <Select
          value={selectedAlgorithm}
          onChange={handleAlgorithmChange}
          className="w-[80%]" 
        >
          <Select.Option value="Steepest Ascent Hill-Climbing">
            Steepest Ascent Hill-Climbing
          </Select.Option>
          <Select.Option value="Hill-Climbing with Sideways Move">
            Hill-Climbing with Sideways Move
          </Select.Option>
          <Select.Option value="Random Restart Hill-Climbing">
            Random Restart Hill-Climbing
          </Select.Option>
          <Select.Option value="Stochastic Hill-Climbing">
            Stochastic Hill-Climbing
          </Select.Option>
          <Select.Option value="Simulated Annealing">
            Simulated Annealing
          </Select.Option>
          <Select.Option value="Genetic Algorithm">
            Genetic Algorithm
          </Select.Option>
        </Select>
        <div className="flex gap-2">
          <Button
            type="primary"
            onClick={handlePlayPause}
            icon={
              isPlaying ? (
                <PauseIcon className="w-4 h-4" />
              ) : (
                <PlayIcon className="w-4 h-4" />
              )
            }
          >
            {isPlaying ? "Pause" : "Play"}
          </Button>
          <Button
            type="default"
            onClick={handleReset}
            icon={<ArrowPathIcon className="w-4 h-4" />}
          />
        </div>
      </ControlRow>

      {/* Sliders for Progress and Playback Speed */}
      <ControlRow>
        <Text
          style={{
            marginBottom: "8px",
            color: "#FFFFFF",
            textAlign: "left",
            width: "45%",
          }}
        >
          Progress Slider:
        </Text>
        <Text
          style={{
            marginBottom: "8px",
            color: "#FFFFFF",
            textAlign: "left",
            width: "45%",
          }}
        >
          Playback Speed:
        </Text>
      </ControlRow>
      <ControlRow>
        <Slider
          min={0}
          max={replayData.length - 1}
          value={currentIndex}
          onChange={handleProgressChange}
          style={{ width: "45%" }}
          handleStyle={{ touchAction: "none" }} 
        />
        <Slider
          min={0.5}
          max={8}
          step={0.1}
          value={speed}
          onChange={onSpeedChange}
          style={{ width: "45%" }}
        />
      </ControlRow>

      {/* Iteration Selection */}
      <Text className="mb-2 text-white text-left w-full">
        Select Iteration:
      </Text>
      <ControlRow>
        <Select
          value={selectedIteration}
          onChange={handleIterationChange}
          className="w-[80%]" // Tailwind class for 50% width
          onMouseDown={(e) => e.stopPropagation()}
        >
          {replayData.map((_, index) => (
            <Select.Option key={index} value={index}>
              Iteration {index + 1}
            </Select.Option>
          ))}
        </Select>
        <Button type="default" onClick={showDetailModal} className="w-[40]">
          Show Details
        </Button>
      </ControlRow>

      {/* Modal for displaying iteration details */}
      <Modal
        title={`Iteration ${selectedIteration + 1} Details`}
        visible={detailVisible}
        onCancel={handleDetailClose}
        footer={null}
      >
        <Table
          dataSource={dataSource}
          columns={columns}
          rowKey="index"
          pagination={false}
        />
      </Modal>
    </GlassContainer>
  );
};

export default FloatingController;
