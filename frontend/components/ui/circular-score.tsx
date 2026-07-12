"use client";

import { motion } from "framer-motion";
import { useEffect, useState } from "react";

interface CircularScoreProps {
  score: number;
  size?: number;
  strokeWidth?: number;
}

export function CircularScore({ score, size = 120, strokeWidth = 10 }: CircularScoreProps) {
  const [animatedScore, setAnimatedScore] = useState(0);
  
  useEffect(() => {
    const timer = setTimeout(() => setAnimatedScore(score), 100);
    return () => clearTimeout(timer);
  }, [score]);

  const radius = (size - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const strokeDashoffset = circumference - (animatedScore / 100) * circumference;

  const getColor = (s: number) => {
    if (s >= 80) return "text-success";
    if (s >= 50) return "text-warning";
    return "text-destructive";
  };

  return (
    <div className="relative flex items-center justify-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="transform -rotate-90">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          className="stroke-muted fill-none"
          strokeWidth={strokeWidth}
        />
        <motion.circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          className={`fill-none ${getColor(score)} transition-colors duration-500`}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset }}
          transition={{ duration: 1.5, ease: "easeOut" }}
          stroke="currentColor"
        />
      </svg>
      <div className="absolute flex flex-col items-center justify-center text-center">
        <span className="text-3xl font-bold tracking-tighter">{animatedScore}</span>
        <span className="text-[10px] uppercase text-muted-foreground font-semibold">Score</span>
      </div>
    </div>
  );
}
