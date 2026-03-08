import { create } from 'zustand';

export interface Notification {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  title?: string;
  message: string;
  autoDismiss?: boolean;
}

interface NotificationStore {
  notifications: Notification[];
  addNotification: (notification: Omit<Notification, 'id'>) => void;
  removeNotification: (id: string) => void;
  clearAll: () => void;
}

export const useNotifications = create<NotificationStore>((set) => ({
  notifications: [],
  
  addNotification: (notification) => {
    const id = `notification-${Date.now()}-${Math.random()}`;
    set((state) => ({
      notifications: [...state.notifications, { ...notification, id }],
    }));
  },
  
  removeNotification: (id) => {
    set((state) => ({
      notifications: state.notifications.filter((n) => n.id !== id),
    }));
  },
  
  clearAll: () => {
    set({ notifications: [] });
  },
}));

// Helper functions for common notification types
export const notify = {
  success: (message: string, title?: string) => {
    useNotifications.getState().addNotification({
      type: 'success',
      title,
      message,
    });
  },
  
  error: (message: string, title?: string) => {
    useNotifications.getState().addNotification({
      type: 'error',
      title,
      message,
    });
  },
  
  warning: (message: string, title?: string) => {
    useNotifications.getState().addNotification({
      type: 'warning',
      title,
      message,
    });
  },
  
  info: (message: string, title?: string) => {
    useNotifications.getState().addNotification({
      type: 'info',
      title,
      message,
    });
  },
};
