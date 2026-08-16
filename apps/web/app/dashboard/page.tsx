'use client';

import React from 'react';
import Sidebar from '@/components/Sidebar';
import Header from '@/components/Header';
import KPICard from '@/components/KPICard';
import ShipmentList from '@/components/ShipmentList';
import { PackageIcon, DocumentCheckIcon, ShieldCheckIcon, ClockIcon } from '@heroicons/react/24/outline';

export default function DashboardPage() {
  return (
    <div className="flex h-screen bg-[#F4F5F7]">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />
        <main className="flex-1 overflow-y-auto p-6">
          <div className="max-w-7xl mx-auto">
            <h1 className="text-[28px] font-bold text-[#111827] mb-6">Dashboard Overview</h1>
            
            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              <KPICard
                title="Active Shipments"
                value="24"
                change="+12%"
                isPositive={true}
                icon={PackageIcon}
              />
              <KPICard
                title="Pending Reviews"
                value="8"
                change="-5%"
                isPositive={true}
                icon={DocumentCheckIcon}
              />
              <KPICard
                title="Compliance Rate"
                value="96.5%"
                change="+2.3%"
                isPositive={true}
                icon={ShieldCheckIcon}
              />
              <KPICard
                title="Avg Processing Time"
                value="2.4 hrs"
                change="-15%"
                isPositive={true}
                icon={ClockIcon}
              />
            </div>

            {/* Main Content Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Recent Shipments */}
              <div className="lg:col-span-2">
                <ShipmentList />
              </div>

              {/* AI Insights Widget */}
              <div className="bg-white rounded-2xl p-6 shadow-sm">
                <h2 className="text-[18px] font-semibold text-[#111827] mb-4">AI Insights</h2>
                <div className="space-y-4">
                  <div className="p-4 bg-[#F4F5F7] rounded-xl">
                    <div className="flex items-start space-x-3">
                      <div className="w-2 h-2 mt-2 rounded-full bg-[#A3E635] flex-shrink-0"></div>
                      <div>
                        <p className="text-sm font-medium text-[#111827]">HS Code Recommendation</p>
                        <p className="text-xs text-[#6B7280] mt-1">Solar panel shipments may qualify for reduced duty under heading 8541.40</p>
                      </div>
                    </div>
                  </div>
                  <div className="p-4 bg-[#F4F5F7] rounded-xl">
                    <div className="flex items-start space-x-3">
                      <div className="w-2 h-2 mt-2 rounded-full bg-[#F59E0B] flex-shrink-0"></div>
                      <div>
                        <p className="text-sm font-medium text-[#111827]">Document Alert</p>
                        <p className="text-xs text-[#6B7280] mt-1">3 shipments missing NRCS certificates for textile imports</p>
                      </div>
                    </div>
                  </div>
                  <div className="p-4 bg-[#F4F5F7] rounded-xl">
                    <div className="flex items-start space-x-3">
                      <div className="w-2 h-2 mt-2 rounded-full bg-[#A3E635] flex-shrink-0"></div>
                      <div>
                        <p className="text-sm font-medium text-[#111827]">Cost Savings</p>
                        <p className="text-xs text-[#6B7280] mt-1">Correct HS classification saved R45,000 in duties this month</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
