# Airport Ground Management System
# Software Testing – Test Cases

## 1. Introduction

Testing is performed to verify that the Airport Ground Management System
works correctly according to the specified functional requirements.

The system was tested module by module, including login, flight management,
gate allocation, ground staff, baggage management, fuel management and reports.

---

## 2. Test Environment

| Item | Details |
|---|---|
| Operating System | Windows |
| Programming Language | Python |
| Backend Framework | Flask |
| Database | MySQL |
| Frontend | HTML, CSS |
| Browser | Google Chrome |
| Development Environment | Visual Studio Code |

---

## 3. Test Cases

### TC-01: Login with Valid Credentials

**Objective:** Verify that a valid user can log into the system.

**Input:**
- Email: admin@airport.com
- Password: admin123

**Expected Result:**  
User should be redirected to the Dashboard.

**Actual Result:**  
User was successfully redirected to the Dashboard.

**Status:** PASS

---

### TC-02: Login with Invalid Credentials

**Objective:** Verify that invalid login credentials are rejected.

**Input:**
- Invalid email/password

**Expected Result:**  
System should display an invalid credentials message.

**Actual Result:**  
Invalid login was rejected.

**Status:** PASS

---

### TC-03: Add Flight

**Objective:** Verify that a new flight can be added.

**Input:**  
Flight details including flight number, airline, origin,
destination, date, time, terminal and status.

**Expected Result:**  
New flight should be stored in the database and displayed
in the Flight Management table.

**Actual Result:**  
Flight was successfully added and displayed.

**Status:** PASS

---

### TC-04: Edit Flight

**Objective:** Verify that existing flight information can be modified.

**Expected Result:**  
Updated flight information should be stored in the database
and displayed in the Flight Management table.

**Actual Result:**  
Flight information was successfully updated.

**Status:** PASS

---

### TC-05: Delete Flight

**Objective:** Verify that an existing flight can be deleted.

**Expected Result:**  
Selected flight should be removed from the Flight Management table.

**Actual Result:**  
Flight was successfully deleted.

**Status:** PASS

---

### TC-06: Add Gate Allocation

**Objective:** Verify that a gate can be assigned to a flight.

**Expected Result:**  
Gate allocation should be stored and displayed in the
Gate Allocation table.

**Actual Result:**  
Gate allocation was successfully created.

**Status:** PASS

---

### TC-07: Prevent Duplicate Active Gate Allocation

**Objective:** Verify that a flight cannot have multiple active gate allocations.

**Expected Result:**  
System should reject the duplicate active allocation.

**Actual Result:**  
Duplicate active gate allocation was prevented.

**Status:** PASS

---

### TC-08: Edit Gate Allocation

**Objective:** Verify that an existing gate allocation can be modified.

**Expected Result:**  
Updated allocation should be stored in the database.

**Actual Result:**  
Gate allocation was successfully updated.

**Status:** PASS

---

### TC-09: Delete Gate Allocation

**Objective:** Verify that a gate allocation can be deleted.

**Expected Result:**  
Selected allocation should be removed from the system.

**Actual Result:**  
Gate allocation was successfully deleted.

**Status:** PASS

---

### TC-10: Add Ground Staff

**Objective:** Verify that a new ground staff member can be added.

**Expected Result:**  
Staff member should be stored in the database and displayed
in the Ground Staff table.

**Actual Result:**  
Ground staff member was successfully added.

**Status:** PASS

---

### TC-11: Edit Ground Staff

**Objective:** Verify that ground staff information can be modified.

**Expected Result:**  
Updated staff information should be displayed.

**Actual Result:**  
Ground staff information was successfully updated.

**Status:** PASS

---

### TC-12: Delete Ground Staff

**Objective:** Verify that a ground staff member can be deleted
when there are no dependent operations.

**Expected Result:**  
Staff member should be removed from the database.

**Actual Result:**  
Ground staff member was successfully deleted when permitted.

**Status:** PASS

---

### TC-13: Add Baggage Record

**Objective:** Verify that baggage information can be added.

**Expected Result:**  
Baggage record should be stored and displayed in the
Baggage Management table.

**Actual Result:**  
Baggage record was successfully added.

**Status:** PASS

---

### TC-14: Edit Baggage Record

**Objective:** Verify that baggage information can be modified.

**Expected Result:**  
Updated baggage information should be displayed.

**Actual Result:**  
Baggage record was successfully updated.

**Status:** PASS

---

### TC-15: Delete Baggage Record

**Objective:** Verify that a baggage record can be deleted.

**Expected Result:**  
Selected baggage record should be removed.

**Actual Result:**  
Baggage record was successfully deleted.

**Status:** PASS

---

### TC-16: Add Fuel Operation

**Objective:** Verify that a fuel operation can be added.

**Expected Result:**  
Fuel operation should be stored and displayed in the
Fuel Management table.

**Actual Result:**  
Fuel operation was successfully added.

**Status:** PASS

---

### TC-17: Edit Fuel Operation

**Objective:** Verify that fuel operation details can be modified.

**Expected Result:**  
Updated fuel information should be displayed.

**Actual Result:**  
Fuel operation was successfully updated.

**Status:** PASS

---

### TC-18: Delete Fuel Operation

**Objective:** Verify that a fuel operation can be deleted.

**Expected Result:**  
Selected fuel operation should be removed.

**Actual Result:**  
Fuel operation was successfully deleted.

**Status:** PASS

---

### TC-19: Reports

**Objective:** Verify that the Reports module displays
system information correctly.

**Expected Result:**  
Reports should display flight, gate, staff, baggage,
fuel and gate allocation statistics.

**Actual Result:**  
Reports were displayed successfully.

**Status:** PASS

---

### TC-20: Navigation

**Objective:** Verify navigation between different system modules.

**Expected Result:**  
Dashboard links should open the corresponding modules correctly.

**Actual Result:**  
All major module links worked correctly.

**Status:** PASS

---

## 4. Testing Summary

| Test Category | Total Tests | Passed | Failed |
|---|---:|---:|---:|
| Authentication | 2 | 2 | 0 |
| Flight Management | 3 | 3 | 0 |
| Gate Allocation | 4 | 4 | 0 |
| Ground Staff | 3 | 3 | 0 |
| Baggage Management | 3 | 3 | 0 |
| Fuel Management | 3 | 3 | 0 |
| Reports | 1 | 1 | 0 |
| Navigation | 1 | 1 | 0 |
| **Total** | **20** | **20** | **0** |

---

## 5. Conclusion

The Airport Ground Management System was tested using
functional test cases covering authentication, flight management,
gate allocation, ground staff management, baggage management,
fuel management, reports and navigation.

All major functional test cases were successfully executed,
and the system performed according to the expected requirements.