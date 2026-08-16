'use client';

import React from 'react';

const shipments = [
  {
    id: 'SHP-2024-001',
    customer: 'SolarTech Industries',
    origin: 'Shanghai, China',
    destination: 'Durban, SA',
    status: 'In Transit',
    statusColor: 'bg-[#3B82F6]',
    value: 'R 450,000',
    date: '2024-01-15',
    items: 'Solar Panels (200 units)',
  },
  {
    id: 'SHP-2024-002',
    customer: 'Textile Imports Ltd',
    origin: 'Mumbai, India',
    destination: 'Cape Town, SA',
    status: 'Pending Review',
    statusColor: 'bg-[#F59E0B]',
    value: 'R 280,000',
    date: '2024-01-14',
    items: 'Cotton Fabric (5000m)',
  },
  {
    id: 'SHP-2024-003',
    customer: 'ElectroWholesale',
    origin: 'Shenzhen, China',
    destination: 'Johannesburg, SA',
    status: 'Cleared',
    statusColor: 'bg-[#10B981]',
    value: 'R 620,000',
    date: '2024-01-13',
    items: 'Electronic Components',
  },
  {
    id: 'SHP-2024-004',
    customer: 'AgriMachinery Co',
    origin: 'São Paulo, Brazil',
    destination: 'Port Elizabeth, SA',
    status: 'Documentation Required',
    statusColor: 'bg-[#EF4444]',
    value: 'R 1,200,000',
    date: '2024-01-12',
    items: 'Agricultural Equipment',
  },
  {
    id: 'SHP-2024-005',
    customer: 'Fashion Forward',
    origin: 'Guangzhou, China',
    destination: 'Durban, SA',
    status: 'In Transit',
    statusColor: 'bg-[#3B82F6]',
    value: 'R 185,000',
    date: '2024-01-11',
    items: 'Apparel (3000 units)',
  },
];

export default function ShipmentList() {
  return (
    <div className="bg-white rounded-2xl shadow-sm">
      <div className="p-6 border-b border-gray-100">
        <div className="flex items-center justify-between">
          <h2 className="text-[18px] font-semibold text-[#111827]">Recent Shipments</h2>
          <button className="text-sm font-medium text-[#A3E635] hover:text-[#8FD12F]">
            View All →
          </button>
        </div>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-[#F4F5F7]">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-[#6B7280] uppercase tracking-wider">
                Shipment ID
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-[#6B7280] uppercase tracking-wider">
                Customer
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-[#6B7280] uppercase tracking-wider">
                Route
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-[#6B7280] uppercase tracking-wider">
                Status
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-[#6B7280] uppercase tracking-wider">
                Value
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-[#6B7280] uppercase tracking-wider">
                Date
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {shipments.map((shipment) => (
              <tr key={shipment.id} className="hover:bg-[#F4F5F7]/50 transition-colors">
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="text-sm font-medium text-[#111827]">{shipment.id}</span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div>
                    <p className="text-sm font-medium text-[#111827]">{shipment.customer}</p>
                    <p className="text-xs text-[#6B7280]">{shipment.items}</p>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm text-[#6B7280]">
                    <p>{shipment.origin}</p>
                    <p className="text-xs text-[#A3E635]">↓</p>
                    <p>{shipment.destination}</p>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium ${
                    shipment.statusColor === 'bg-[#10B981]' ? 'bg-[#10B981]/10 text-[#10B981]' :
                    shipment.statusColor === 'bg-[#3B82F6]' ? 'bg-[#3B82F6]/10 text-[#3B82F6]' :
                    shipment.statusColor === 'bg-[#F59E0B]' ? 'bg-[#F59E0B]/10 text-[#F59E0B]' :
                    'bg-[#EF4444]/10 text-[#EF4444]'
                  }`}>
                    <span className={`w-1.5 h-1.5 rounded-full mr-1.5 ${shipment.statusColor}`}></span>
                    {shipment.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="text-sm font-medium text-[#111827]">{shipment.value}</span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="text-sm text-[#6B7280]">{shipment.date}</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
