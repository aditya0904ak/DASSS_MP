
import React from 'react';
import { format } from 'date-fns';

const ActivityLog = ({ events }) => {
  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm h-full overflow-hidden flex flex-col">
      <h3 className="text-sm font-bold text-slate-800 uppercase tracking-widest mb-6">Recent System Activity</h3>
      
      <div className="flex-1 overflow-y-auto pr-2">
        <div className="relative border-l-2 border-slate-100 ml-3 space-y-6 pb-2">
          {events.length === 0 ? (
            <p className="text-xs text-slate-400 pl-4">No recent activity.</p>
          ) : (
            events.map((event, i) => (
              <div key={i} className="relative pl-6">
                <div className={`absolute -left-1.5 top-1.5 w-3 h-3 rounded-full border-2 border-white ${event.type === 'error' ? 'bg-red-500' : 'bg-emerald-500'}`}></div>
                <p className="text-xs font-bold text-slate-400 mb-1">{format(new Date(event.time), 'HH:mm:ss')}</p>
                <p className="text-sm font-medium text-slate-700">{event.message}</p>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default ActivityLog;
