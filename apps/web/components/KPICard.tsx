'use client';

import React from 'react';

interface KPICardProps {
  title: string;
  value: string;
  change: string;
  isPositive: boolean;
  icon: React.ComponentType<{ className?: string }>;
}

export default function KPICard({ title, value, change, isPositive, icon: Icon }: KPICardProps) {
  return (
    <div className="bg-white rounded-2xl p-6 shadow-sm hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between mb-4">
        <div className="w-12 h-12 bg-[#F4F5F7] rounded-xl flex items-center justify-center">
          <Icon className="w-6 h-6 text-[#A3E635]" />
        </div>
        <div className={`flex items-center px-2.5 py-1 rounded-full text-xs font-medium ${
          isPositive 
            ? 'bg-[#10B981]/10 text-[#10B981]' 
            : 'bg-[#EF4444]/10 text-[#EF4444]'
        }`}>
          {change}
        </div>
      </div>
      <h3 className="text-[#6B7280] text-sm font-medium mb-1">{title}</h3>
      <p className="text-[28px] font-bold text-[#111827]">{value}</p>
    </div>
  );
}
