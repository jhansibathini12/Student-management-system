/**
 * Student Management System - Main JavaScript
 * Handles sidebar toggles, delete confirmation modals, and alert dismissal.
 */

document.addEventListener('DOMContentLoaded', function () {
  // 1. Sidebar Toggle for Mobile View
  const sidebar = document.getElementById('sidebar');
  const sidebarToggle = document.getElementById('sidebarToggle');
  const sidebarOverlay = document.getElementById('sidebarOverlay');

  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', function () {
      sidebar.classList.toggle('show');
      if (sidebarOverlay) {
        sidebarOverlay.classList.toggle('d-none');
      }
    });
  }

  if (sidebarOverlay && sidebar) {
    sidebarOverlay.addEventListener('click', function () {
      sidebar.classList.remove('show');
      sidebarOverlay.classList.add('d-none');
    });
  }

  // 2. Delete Confirmation Modal Setup
  const deleteModal = document.getElementById('deleteConfirmModal');
  if (deleteModal) {
    deleteModal.addEventListener('show.bs.modal', function (event) {
      // Button that triggered the modal
      const button = event.relatedTarget;
      if (!button) return;

      const studentId = button.getAttribute('data-student-id');
      const studentName = button.getAttribute('data-student-name');
      const deleteUrl = button.getAttribute('data-delete-url');

      // Update the modal's content
      const modalStudentName = deleteModal.querySelector('#modalStudentName');
      const modalStudentId = deleteModal.querySelector('#modalStudentId');
      const deleteForm = deleteModal.querySelector('#deleteStudentForm');

      if (modalStudentName) modalStudentName.textContent = studentName || 'Selected Student';
      if (modalStudentId) modalStudentId.textContent = studentId || '';
      if (deleteForm && deleteUrl) deleteForm.setAttribute('action', deleteUrl);
    });
  }

  // 3. Auto-dismiss alerts after 5 seconds
  const autoDismissAlerts = document.querySelectorAll('.alert.alert-dismissible');
  autoDismissAlerts.forEach(function (alertElement) {
    setTimeout(function () {
      const alert = bootstrap.Alert.getOrCreateInstance(alertElement);
      if (alert) {
        alert.close();
      }
    }, 5000);
  });

  // 4. Initialize all Bootstrap tooltips if present
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });
});
