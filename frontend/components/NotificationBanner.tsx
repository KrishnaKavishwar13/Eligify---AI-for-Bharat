'use client';

import { useEffect } from 'react';
import { X, CheckCircle, AlertCircle, Info, AlertTriangle } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useNotifications } from '@/hooks/useNotifications';

export default function NotificationBanner() {
  const { notifications, removeNotification } = useNotifications();

  useEffect(() => {
    // Auto-dismiss notifications after 5 seconds
    notifications.forEach((notification) => {
      if (notification.autoDismiss !== false) {
        const timer = setTimeout(() => {
          removeNotification(notification.id);
        }, 5000);

        return () => clearTimeout(timer);
      }
    });
  }, [notifications, removeNotification]);

  if (notifications.length === 0) return null;

  return (
    <div className="fixed right-4 top-4 z-50 flex flex-col gap-2">
      {notifications.map((notification) => {
        const config = {
          success: {
            icon: CheckCircle,
            bg: 'bg-green-50',
            border: 'border-success',
            text: 'text-green-900',
            iconColor: 'text-success',
          },
          error: {
            icon: AlertCircle,
            bg: 'bg-red-50',
            border: 'border-danger',
            text: 'text-red-900',
            iconColor: 'text-danger',
          },
          warning: {
            icon: AlertTriangle,
            bg: 'bg-yellow-50',
            border: 'border-warning',
            text: 'text-yellow-900',
            iconColor: 'text-warning',
          },
          info: {
            icon: Info,
            bg: 'bg-blue-50',
            border: 'border-primary',
            text: 'text-blue-900',
            iconColor: 'text-primary',
          },
        }[notification.type];

        const Icon = config.icon;

        return (
          <div
            key={notification.id}
            className={cn(
              'flex w-96 items-start gap-3 rounded-lg border-l-4 p-4 shadow-lg',
              config.bg,
              config.border,
              'animate-in slide-in-from-right duration-300'
            )}
          >
            <Icon className={cn('h-5 w-5 flex-shrink-0', config.iconColor)} />
            <div className="flex-1">
              {notification.title && (
                <p className={cn('font-semibold', config.text)}>
                  {notification.title}
                </p>
              )}
              <p className={cn('text-sm', config.text)}>
                {notification.message}
              </p>
            </div>
            <button
              onClick={() => removeNotification(notification.id)}
              className={cn(
                'rounded-lg p-1 hover:bg-white/50',
                config.text
              )}
            >
              <X className="h-4 w-4" />
            </button>
          </div>
        );
      })}
    </div>
  );
}
