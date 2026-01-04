/**
 * Job Seeker Dashboard - Production Ready
 * Integrated with Backend APIs & Design System
 */

const JobseekerDashboard = {
  /**
   * Initialize job seeker dashboard
   */
  async init() {
    // Initialize base dashboard first (handles sidebar/user menu toggles)
    if (typeof DashboardBase !== 'undefined') {
      await DashboardBase.init();
    }

    // Load dynamic dashboard data from backend
    await this.loadDashboardData();
  },

  /**
   * Load dashboard data from multiple endpoints
   */
  async loadDashboardData() {
    // Show loading states for smooth UX
    this.setLoading(true);

    try {
      // Execute all fetches in parallel for performance
      await Promise.all([
        this.loadAppliedJobs(),
        this.loadNotifications(),
        this.updateKPIs()
      ]);
    } catch (error) {
      console.error('Dashboard data sync failed:', error);
    } finally {
      this.setLoading(false);
    }
  },

  /**
   * Fetch and render applied jobs
   */
  async loadAppliedJobs() {
    const container = document.getElementById('appliedJobsTable');
    if (!container) return;

    try {
      // Real API Call
      const response = await fetch('/api/jobseeker/applications');
      const applications = await response.json();

      if (!applications || applications.length === 0) {
        this.renderEmptyState(container, '📋', 'No applications yet', 'Start browsing jobs to apply!');
        return;
      }

      // Render table rows
      container.innerHTML = applications.map(app => `
        <tr>
          <td><strong class="text-on-light">${app.job_title}</strong></td>
          <td class="text-on-light-secondary">${app.company}</td>
          <td>${this.getStatusBadge(app.status)}</td>
          <td class="text-on-light-secondary">${this.formatDate(app.applied_date)}</td>
          <td>
            <button class="btn btn-sm btn-secondary" onclick="JobseekerDashboard.viewApplication(${app.id})">
              View
            </button>
          </td>
        </tr>
      `).join('');
    } catch (error) {
      container.innerHTML = '<tr><td colspan="5" class="error-text">Failed to load applications.</td></tr>';
    }
  },

  /**
   * Fetch and update KPI cards dynamically
   */
  async updateKPIs() {
    try {
      const response = await fetch('/api/jobseeker/stats');
      const stats = await response.json();

      // Mapping IDs to data keys
      const kpiMap = {
        'kpiTotalApplications': stats.total || 0,
        'kpiPendingApplications': stats.pending || 0,
        'kpiAcceptedApplications': stats.accepted || 0,
        'kpiRejectedApplications': stats.rejected || 0
      };

      Object.keys(kpiMap).forEach(id => {
        const el = document.getElementById(id);
        if (el) el.textContent = kpiMap[id];
      });
    } catch (error) {
      console.warn('Could not update KPIs');
    }
  },

  /**
   * Utility: Get status badge with design tokens
   */
  getStatusBadge(status) {
    const statusLower = status.toLowerCase();
    const badges = {
      pending: '<span class="badge badge-warning">Pending</span>',
      accepted: '<span class="badge badge-success">Accepted</span>',
      rejected: '<span class="badge badge-error">Rejected</span>',
      interviewing: '<span class="badge badge-info">Interview</span>'
    };
    return badges[statusLower] || '<span class="badge badge-neutral">Unknown</span>';
  },

  /**
   * Utility: Standardized Empty State Renderer
   */
  renderEmptyState(container, icon, title, text) {
    container.innerHTML = `
      <tr>
        <td colspan="5" class="empty-state-cell">
          <div class="empty-state">
            <div class="empty-state-icon">${icon}</div>
            <div class="empty-state-title">${title}</div>
            <div class="empty-state-text">${text}</div>
          </div>
        </td>
      </tr>
    `;
  },

  /**
   * Global Loading State UI
   */
  setLoading(isLoading) {
    const main = document.querySelector('.dashboard-main');
    if (main) {
      isLoading ? main.classList.add('loading-fade') : main.classList.remove('loading-fade');
    }
  },

  formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short', day: 'numeric', year: 'numeric'
    });
  },

  viewApplication(id) {
    window.location.href = `/applications/${id}`;
  }
};

// Auto-init based on URL
document.addEventListener('DOMContentLoaded', () => {
  if (window.location.pathname.includes('/jobseeker')) {
    JobseekerDashboard.init();
  }
});

if (typeof window !== 'undefined') {
  window.JobseekerDashboard = JobseekerDashboard;
}