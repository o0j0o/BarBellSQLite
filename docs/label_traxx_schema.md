# Label Traxx (LT64) Schema Inventory

Total tables/views reported by SQLTables: 270
Columns successfully enumerated for: 270 table(s)
Not reachable (SQLColumns failed): 0 table(s)

## Server SQL dialect notes

- **Row limiting: `LIMIT` is accepted** (`SELECT * FROM Ticket LIMIT 1`); `TOP` was never needed.
- **Every ID-like column is CLOB (text)**, even where values look numeric (e.g. `'122984'`). A bare numeric literal in a WHERE clause fails (`08004 ... Failed to execute statement (1108)`) - always quote values as strings.
- **No double-quoted identifiers were needed** - every table/column name encountered is a plain CamelCase token, no spaces or reserved words.
- Complex joins/subqueries were avoided as expected for the 4D SQL subset - `Ticket`, `Product`, `TicketItem` were queried separately and joined in Python.

## All tables reported by SQLTables

| table_cat | table_schem | table_name | table_type |
|---|---|---|---|
| None | None | ABC_Event | TABLE |
| None | None | ABC_Log | TABLE |
| None | None | AccountingForms | TABLE |
| None | None | Active4D | TABLE |
| None | None | Activity | TABLE |
| None | None | Address | TABLE |
| None | None | Affiliate | TABLE |
| None | None | AP_Aging_Invoice | TABLE |
| None | None | AP_Aging_Invoice_Historical | TABLE |
| None | None | AP_Aging_Supplier | TABLE |
| None | None | AP_Aging_Supplier_Historical | TABLE |
| None | None | AP_Balance | TABLE |
| None | None | AP_Balance_Fat | TABLE |
| None | None | AP_BankAccount | TABLE |
| None | None | AP_BankReconciliation | TABLE |
| None | None | AP_Check_Register | TABLE |
| None | None | AP_Check_Run | TABLE |
| None | None | AP_Check_Run_Detail | TABLE |
| None | None | AP_Check_Run_TempChecks | TABLE |
| None | None | AP_Checks_VoidedGL_Lines | TABLE |
| None | None | AP_Checks_VoidedInfo | TABLE |
| None | None | AP_Constants | TABLE |
| None | None | AP_Hand_Checks | TABLE |
| None | None | AP_Hand_Checks_AP | TABLE |
| None | None | AP_Hand_Checks_GL | TABLE |
| None | None | AP_Invoice | TABLE |
| None | None | AP_Invoice_Line | TABLE |
| None | None | AP_Invoice_Tax | TABLE |
| None | None | AP_Maint_ApplyTo_AP | TABLE |
| None | None | AP_Maint_ApplyTo_GL | TABLE |
| None | None | AP_Maintenance | TABLE |
| None | None | AP_Transaction | TABLE |
| None | None | API_Registry | TABLE |
| None | None | API_Servers | TABLE |
| None | None | API_Templates | TABLE |
| None | None | AR_Aging_CustCollectNotes | TABLE |
| None | None | AR_Aging_Customer | TABLE |
| None | None | AR_Aging_Customer_Historical | TABLE |
| None | None | AR_Aging_Invoice | TABLE |
| None | None | AR_Aging_Invoice_Historical | TABLE |
| None | None | AR_Balance | TABLE |
| None | None | AR_Balance_FAT | TABLE |
| None | None | AR_CreditCardAccounts | TABLE |
| None | None | AR_Maint_ApplyTo_AR | TABLE |
| None | None | AR_Maint_ApplyTo_GL | TABLE |
| None | None | AR_Maintenance | TABLE |
| None | None | AR_Transaction | TABLE |
| None | None | Associate | TABLE |
| None | None | Banks_list | TABLE |
| None | None | BB_Misc | TABLE |
| None | None | Blob_Chunk | TABLE |
| None | None | Budget_AssociateSales | TABLE |
| None | None | Budget_CustomerSales | TABLE |
| None | None | CDF_Definition | TABLE |
| None | None | CDF_ListValues | TABLE |
| None | None | CDF_Values | TABLE |
| None | None | Constants | TABLE |
| None | None | Contact | TABLE |
| None | None | CR_ApplyTo_AR | TABLE |
| None | None | CR_ApplyTo_GL | TABLE |
| None | None | CR_Checks | TABLE |
| None | None | CR_Deposit | TABLE |
| None | None | CRON_Event_Log | TABLE |
| None | None | CRON_Job | TABLE |
| None | None | Customer | TABLE |
| None | None | CustomerProduct | TABLE |
| None | None | DASH_Goal | TABLE |
| None | None | DASH_Goal_Bundle | TABLE |
| None | None | DASH_Graph | TABLE |
| None | None | DASH_Graph_Group | TABLE |
| None | None | DASH_Preference | TABLE |
| None | None | deleteTrackingLog | TABLE |
| None | None | Dialogs | TABLE |
| None | None | DieChart | TABLE |
| None | None | DieChart_Item | TABLE |
| None | None | DieHardnessRates | TABLE |
| None | None | DupTemp | TABLE |
| None | None | EmailObjects | TABLE |
| None | None | Employee_Preference | TABLE |
| None | None | EmployeeStatus | TABLE |
| None | None | Empty_Multiuser | TABLE |
| None | None | Encoder_License | TABLE |
| None | None | EP_ElectronicPayments | TABLE |
| None | None | EP_ItemsPaid | TABLE |
| None | None | EP_SupplierTotals | TABLE |
| None | None | Equip_InkTypesAndRates | TABLE |
| None | None | Equip_RatesByNumberOfColors | TABLE |
| None | None | Equip_SemiRotary | TABLE |
| None | None | Equip_UserDefined | TABLE |
| None | None | Equipment | TABLE |
| None | None | Est_AddlStock | TABLE |
| None | None | Est_PostPress | TABLE |
| None | None | Est_PriceTuner | TABLE |
| None | None | Est_Tools | TABLE |
| None | None | Est_UserDefined | TABLE |
| None | None | Estimate | TABLE |
| None | None | Estimate_Activity | TABLE |
| None | None | ETraxx_Constants | TABLE |
| None | None | ETraxx_Email | TABLE |
| None | None | ETraxx_Estimate | TABLE |
| None | None | ETraxx_Log | TABLE |
| None | None | ETraxx_Prospect | TABLE |
| None | None | ETraxx_Website_Text | TABLE |
| None | None | EXT_FileStorage | TABLE |
| None | None | EXT_Reference | TABLE |
| None | None | ForeignCurrency | TABLE |
| None | None | ForeignCurrency_Rate | TABLE |
| None | None | Freight_Chart | TABLE |
| None | None | FS_CashFlowClasses | TABLE |
| None | None | FS_FinancialStatements | TABLE |
| None | None | GL_Account_Balances | TABLE |
| None | None | GL_AccountingConstants | TABLE |
| None | None | GL_AccountingYears | TABLE |
| None | None | GL_Analysis_View | TABLE |
| None | None | GL_AssignGLDistribution | TABLE |
| None | None | GL_Balances_Access | TABLE |
| None | None | GL_Budgets | TABLE |
| None | None | GL_Budgets_Accounts | TABLE |
| None | None | GL_ChartOfAccounts | TABLE |
| None | None | GL_COA_FAT | TABLE |
| None | None | GL_Detail_Activity | TABLE |
| None | None | GL_NetIncome | TABLE |
| None | None | GL_ProfitCenter | TABLE |
| None | None | GL_View_Accounts | TABLE |
| None | None | glPrefixConst | TABLE |
| None | None | HoursOff | TABLE |
| None | None | HP_PrintOS | TABLE |
| None | None | HP_PrintOS_InkSub | TABLE |
| None | None | HP_PrintOS_Prefs | TABLE |
| None | None | HP_PrintOS_storedData | TABLE |
| None | None | Http_Client_queue | TABLE |
| None | None | HTTP_Log | TABLE |
| None | None | InkInventory | TABLE |
| None | None | InOutStatus | TABLE |
| None | None | Inspection | TABLE |
| None | None | IntercompanyTransferTemplate | TABLE |
| None | None | Invent_Adj_Log | TABLE |
| None | None | Inventory | TABLE |
| None | None | Inventory_Item | TABLE |
| None | None | Inventory_Level | TABLE |
| None | None | InventoryLog | TABLE |
| None | None | Invoice | TABLE |
| None | None | Invoice_GL_Distribution | TABLE |
| None | None | Invoice_Tax_Detail | TABLE |
| None | None | Invoice_Tax_PackSlip | TABLE |
| None | None | InvoiceItem | TABLE |
| None | None | JDF_AE10_ColorStrategy | TABLE |
| None | None | JDF_Constants | TABLE |
| None | None | JE_JournalEntry | TABLE |
| None | None | JE_JournalEntryLine | TABLE |
| None | None | Keys | TABLE |
| None | None | Keys_Subscription | TABLE |
| None | None | Kit_Recipe | TABLE |
| None | None | Knowledge | TABLE |
| None | None | Labels | TABLE |
| None | None | Language_Item | TABLE |
| None | None | Large_Objects | TABLE |
| None | None | Launch_History | TABLE |
| None | None | List | TABLE |
| None | None | Logs | TABLE |
| None | None | LWFile | TABLE |
| None | None | Maintenance | TABLE |
| None | None | MarketingCategory | TABLE |
| None | None | MasterInvoice_Detail | TABLE |
| None | None | MasterInvoice_POs | TABLE |
| None | None | masterPS | TABLE |
| None | None | Material_Use | TABLE |
| None | None | MenuReports | TABLE |
| None | None | MFGRep | TABLE |
| None | None | multiLocation | TABLE |
| None | None | multiLocation_Main | TABLE |
| None | None | OAuth2 | TABLE |
| None | None | PackingSlip | TABLE |
| None | None | PackSlipItem | TABLE |
| None | None | Patch_History | TABLE |
| None | None | Payment | TABLE |
| None | None | Payment_Terms | TABLE |
| None | None | PO_Item_Stock | TABLE |
| None | None | PO_Stock_eReceiptRolls | TABLE |
| None | None | PO_Stock_eReceiptShip | TABLE |
| None | None | PO_Stock_PackListXML | TABLE |
| None | None | POItems | TABLE |
| None | None | Pop_Localization | TABLE |
| None | None | PostPress_LineItem | TABLE |
| None | None | Press_Sensor_Status | TABLE |
| None | None | Price | TABLE |
| None | None | Prod_AddlStock | TABLE |
| None | None | Prod_UserDefined | TABLE |
| None | None | Product | TABLE |
| None | None | Product_BillOfMaterials | TABLE |
| None | None | Product_GL_Distribution | TABLE |
| None | None | Product_Inventory | TABLE |
| None | None | Product_PostPress | TABLE |
| None | None | Product_Tools | TABLE |
| None | None | ProductColor | TABLE |
| None | None | ProfitAdjust | TABLE |
| None | None | Project_Affiliate | TABLE |
| None | None | Project_Control | TABLE |
| None | None | Project_Data | TABLE |
| None | None | PurchaseOrder | TABLE |
| None | None | PurchaseOrder_Items | TABLE |
| None | None | QP_Event | TABLE |
| None | None | Quality_Log | TABLE |
| None | None | Quality_Procedure | TABLE |
| None | None | remoteDataCapture | TABLE |
| None | None | Reports | TABLE |
| None | None | RollStock | TABLE |
| None | None | RotoMetrics_LOV_Codes | TABLE |
| None | None | RotoMetricsPressIDs | TABLE |
| None | None | SalesTax_Preferences | TABLE |
| None | None | SalesTax_Regions | TABLE |
| None | None | SalesTax_RegionTypes | TABLE |
| None | None | SalesTax_TaxTypes | TABLE |
| None | None | SalesTax_VAT_Codes | TABLE |
| None | None | SC_Actions | TABLE |
| None | None | SC_Equipment_Downtime | TABLE |
| None | None | SC_Equipment_group | TABLE |
| None | None | SC_Equipment_group_Items | TABLE |
| None | None | SC_Event | TABLE |
| None | None | SC_MasterEvent | TABLE |
| None | None | SC_Preferences | TABLE |
| None | None | SC_Shifts | TABLE |
| None | None | SC_Time_Card | TABLE |
| None | None | Schedule_EquipGroup | TABLE |
| None | None | ScheduleDay | TABLE |
| None | None | ScheduleDetail | TABLE |
| None | None | Settings | TABLE |
| None | None | SP_Inventory_Add | TABLE |
| None | None | SP_Inventory_Release | TABLE |
| None | None | Stock | TABLE |
| None | None | StockInventory | TABLE |
| None | None | StockProduct | TABLE |
| None | None | StockProduct_XML_Order | TABLE |
| None | None | Supplier | TABLE |
| None | None | Supplier_Activity | TABLE |
| None | None | Supplier_Contact | TABLE |
| None | None | Supplier_eCommerce | TABLE |
| None | None | Supplier_GL_Defaults | TABLE |
| None | None | Table_oc | TABLE |
| None | None | Tax_Adjustments | TABLE |
| None | None | Tax_CashBasis_Payments | TABLE |
| None | None | Tax_CashBasis_Receipts | TABLE |
| None | None | Template_4D_Write | TABLE |
| None | None | Ticket | TABLE |
| None | None | Ticket_Activity | TABLE |
| None | None | Ticket_BillOfMaterials | TABLE |
| None | None | Ticket_CommonStock | TABLE |
| None | None | Ticket_FilePlan | TABLE |
| None | None | Ticket_JDF_Out | TABLE |
| None | None | Ticket_Tools | TABLE |
| None | None | Ticket_UserDefined | TABLE |
| None | None | TicketItem | TABLE |
| None | None | TickItmStatus_to_AE_Event | TABLE |
| None | None | TimeCard | TABLE |
| None | None | TimeCard_Operation | TABLE |
| None | None | TLI_Status | TABLE |
| None | None | Tool_Maintenance | TABLE |
| None | None | Tooling | TABLE |
| None | None | transitRequest | TABLE |
| None | None | TraxxLink_PackingSlip_Log | TABLE |
| None | None | UEFs | TABLE |
| None | None | UK_VAT | TABLE |
| None | None | UniqueIDFile | TABLE |
| None | None | UploadControl | TABLE |
| None | None | UploadData | TABLE |
| None | None | UserFavorites | TABLE |
| None | None | WIP_Parentage | TABLE |
| None | None | WorldshipData | TABLE |
| None | None | ZeroRec | TABLE |
| None | None | ZRec | TABLE |

## Columns per reachable table

### ABC_Event

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| Activity | CLOB | 30 | 1 |
| Description | CLOB | 0 | 1 |
| Capacity | REAL | 7 | 1 |
| Rate_1 | REAL | 7 | 1 |
| Rate_2 | REAL | 7 | 1 |
| Rate_3 | REAL | 7 | 1 |
| Disabled | BOOLEAN | 5 | 1 |
| PK_UUID | UUID | 0 | 1 |

### ABC_Log

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| Activity | CLOB | 30 | 1 |
| Log_Table_Number | INT32 | 11 | 1 |
| Log_Table_Name | CLOB | 31 | 1 |
| Log_Record_ID | CLOB | 15 | 1 |
| Customer_ID | CLOB | 10 | 1 |
| Customer_Name | CLOB | 80 | 1 |
| Associate_Number | CLOB | 10 | 1 |
| Associate_Name | CLOB | 60 | 1 |
| Start_Date | TIMESTAMP | 19 | 1 |
| Start_Time | INTERVAL | 10 | 1 |
| End_Date | TIMESTAMP | 19 | 1 |
| End_Time | INTERVAL | 10 | 1 |
| Elapsed_Time | INTERVAL | 10 | 1 |
| Rate_Title | CLOB | 40 | 1 |
| Rate | REAL | 7 | 1 |
| Cost | REAL | 7 | 1 |
| Change_Log | CLOB | 0 | 1 |
| EnteredBy | CLOB | 50 | 1 |
| ModifiedBy | CLOB | 50 | 1 |
| EnteredDate | TIMESTAMP | 19 | 1 |
| ModifiedDate | TIMESTAMP | 19 | 1 |
| EnteredTime | INTERVAL | 10 | 1 |
| ModifiedTime | INTERVAL | 10 | 1 |
| PK_UUID | UUID | 0 | 1 |

### API_Registry

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| PK_UUID | UUID | 0 | 1 |
| API_template | UUID | 0 | 1 |
| API_Client | CLOB | 255 | 1 |
| Server_ip | CLOB | 0 | 1 |
| Last_Updated | CLOB | 20 | 1 |
| Message | CLOB | 255 | 1 |
| API_Server | UUID | 0 | 1 |
| Created | CLOB | 20 | 1 |

### API_Servers

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| PK_UUID | UUID | 0 | 1 |
| Created_DTS | CLOB | 16 | 1 |
| Modified_DTS | CLOB | 16 | 1 |
| Client_Name | CLOB | 255 | 1 |
| Server_Address | CLOB | 255 | 1 |
| Selected | BOOLEAN | 5 | 1 |

### API_Templates

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| PK_UUID | UUID | 0 | 1 |
| Created_DTS | CLOB | 16 | 1 |
| Modified_DTS | CLOB | 16 | 1 |
| Response_Type | CLOB | 12 | 1 |
| Code | CLOB | 0 | 1 |
| Name | CLOB | 80 | 1 |
| Description | CLOB | 0 | 1 |
| Created_Employee_ID | CLOB | 10 | 1 |
| Created_by | CLOB | 80 | 1 |
| Modified_by | CLOB | 80 | 1 |
| ID | CLOB | 255 | 1 |
| Created_Date | TIMESTAMP | 19 | 1 |
| Created_Time | INTERVAL | 10 | 1 |
| Modified_Date | TIMESTAMP | 19 | 1 |
| Modified_Time | INTERVAL | 10 | 1 |
| Modified_Employee_ID | CLOB | 10 | 1 |
| Request_with_JSON_Content | BOOLEAN | 5 | 1 |
| On_schedule | BOOLEAN | 5 | 1 |
| Last_Execution | CLOB | 20 | 1 |
| Execute_every_days | INT16 | 6 | 1 |
| Execute_every_Hours | INT16 | 6 | 1 |
| Execute_Every_Minutes | INT32 | 11 | 1 |
| Next_Execution | CLOB | 20 | 1 |
| Interpreter | CLOB | 20 | 1 |
| SSL_Req | BOOLEAN | 5 | 1 |
| USER_Password_Req | BOOLEAN | 5 | 1 |
| Restricted_IP | BOOLEAN | 5 | 1 |
| Users | None | 0 | 1 |
| Passwords | None | 0 | 1 |
| IP | None | 0 | 1 |
| Category | CLOB | 20 | 1 |
| Version | CLOB | 10 | 1 |
| Execute_at_time | INTERVAL | 10 | 1 |
| Execute_Now | BOOLEAN | 5 | 1 |
| Last_Updated | CLOB | 20 | 1 |
| LabelTraxx_version | CLOB | 20 | 1 |
| Encrypt | BOOLEAN | 5 | 1 |
| Encrypt_Method | CLOB | 255 | 1 |
| Encrypt_Password | CLOB | 255 | 1 |
| RollBack_Code | CLOB | 0 | 1 |
| RollBack_version | CLOB | 10 | 1 |
| RollBack_Others | None | 0 | 1 |
| Code_Updated | CLOB | 20 | 1 |
| Passwords_Encypted | BOOLEAN | 5 | 1 |
| Http_Client_Q | BOOLEAN | 5 | 1 |
| Http_Client_Q_Request | None | 0 | 1 |

### AP_Aging_Invoice

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| Invoice_Number | CLOB | 20 | 1 |
| AP_Balance_ID | INT32 | 11 | 1 |
| Supplier_ID | INT32 | 11 | 1 |
| BalanceDue | REAL | 7 | 1 |
| Aging_Current | REAL | 7 | 1 |
| Aging_Over30 | REAL | 7 | 1 |
| Aging_Over60 | REAL | 7 | 1 |
| Aging_Over90 | REAL | 7 | 1 |
| Supplier_Name | CLOB | 80 | 1 |
| Invoice_Date | TIMESTAMP | 19 | 1 |
| SupplierNameNumKey | CLOB | 60 | 1 |
| AP_Invoice_ID | INT32 | 11 | 1 |
| DueDate | TIMESTAMP | 19 | 1 |
| PK_UUID | UUID | 0 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |

### AP_Aging_Invoice_Historical

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| Invoice_Number | CLOB | 20 | 1 |
| AP_Balance_ID | INT32 | 11 | 1 |
| Supplier_ID | INT32 | 11 | 1 |
| Supplier_Name | CLOB | 50 | 1 |
| BalanceDue | REAL | 7 | 1 |
| Aging_Current | REAL | 7 | 1 |
| Aging_Over30 | REAL | 7 | 1 |
| Aging_Over60 | REAL | 7 | 1 |
| Aging_Over90 | REAL | 7 | 1 |
| Invoice_Date | TIMESTAMP | 19 | 1 |
| SupplierNameNumKey | CLOB | 60 | 1 |
| DueDate | TIMESTAMP | 19 | 1 |
| PK_UUID | UUID | 0 | 1 |

### AP_Aging_Supplier

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| Supplier_ID | INT32 | 11 | 1 |
| BalanceDue | REAL | 7 | 1 |
| Aging_Current | REAL | 7 | 1 |
| Aging_Over30 | REAL | 7 | 1 |
| Aging_Over60 | REAL | 7 | 1 |
| Aging_Over90 | REAL | 7 | 1 |
| Supplier_Name | CLOB | 80 | 1 |
| PK_UUID | UUID | 0 | 1 |

### AP_Aging_Supplier_Historical

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| Supplier_ID | INT32 | 11 | 1 |
| Supplier_Name | CLOB | 50 | 1 |
| BalanceDue | REAL | 7 | 1 |
| Aging_Current | REAL | 7 | 1 |
| Aging_Over30 | REAL | 7 | 1 |
| Aging_Over60 | REAL | 7 | 1 |
| Aging_Over90 | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |

### AP_Balance

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| Invoice_Number | CLOB | 20 | 1 |
| Invoice_Date | TIMESTAMP | 19 | 1 |
| DueDate | TIMESTAMP | 19 | 1 |
| Supplier_ID | INT32 | 11 | 1 |
| Supplier_Name | CLOB | 80 | 1 |
| OriginalAmountDue | REAL | 7 | 1 |
| BalanceDue | REAL | 7 | 1 |
| DiscountAmount | REAL | 7 | 1 |
| DiscountDate | TIMESTAMP | 19 | 1 |
| Source | CLOB | 20 | 1 |
| IncludeInAverageDaysPaid | CLOB | 20 | 1 |
| SupplierNameNumKey | CLOB | 60 | 1 |
| DatePaidOff | TIMESTAMP | 19 | 1 |
| AP_Invoice_ID | INT32 | 11 | 1 |
| PostToDate | TIMESTAMP | 19 | 1 |
| FCT_OriginalAmtDue | REAL | 7 | 1 |
| FCT_BalanceDue | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |
| paymentType | CLOB | 45 | 1 |
| glPrefix | CLOB | 3 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |

### AP_Balance_Fat

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| AP_Balance_ID | INT32 | 11 | 1 |
| Notes | CLOB | 0 | 1 |
| PK_UUID | UUID | 0 | 1 |

### AP_BankAccount

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| AccountName | CLOB | 30 | 1 |
| BankName | CLOB | 30 | 1 |
| BankAccountNumber | CLOB | 30 | 1 |
| GL_Acct_Number | CLOB | 13 | 1 |
| Description | CLOB | 0 | 1 |
| CheckFormat | CLOB | 30 | 1 |
| LastCheckNumber | INT32 | 11 | 1 |
| EnteredBy | CLOB | 50 | 1 |
| EnteredDate | TIMESTAMP | 19 | 1 |
| ModifiedBy | CLOB | 50 | 1 |
| ModifiedDate | TIMESTAMP | 19 | 1 |
| Inactive | BOOLEAN | 5 | 1 |
| GL_Acct_Name | CLOB | 40 | 1 |
| EnteredTime | INTERVAL | 10 | 1 |
| ModifiedTime | INTERVAL | 10 | 1 |
| GL_Acct_Name_BankFees | CLOB | 40 | 1 |
| GL_Acct_Num_BankFees | CLOB | 13 | 1 |
| Bank_ID | INT32 | 11 | 1 |
| Foreign_country | BOOLEAN | 5 | 1 |
| PK_UUID | UUID | 0 | 1 |
| Foreign_Currency_ID | INT32 | 11 | 1 |
| DynamicCheckForm | CLOB | 0 | 1 |

### AP_BankReconciliation

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| BankAccount_ID | INT32 | 11 | 1 |
| BankAccount_Name | CLOB | 30 | 1 |
| BeginningDate | TIMESTAMP | 19 | 1 |
| EndingDate | TIMESTAMP | 19 | 1 |
| EndingBankBalance | REAL | 7 | 1 |
| EndingBookBalance | REAL | 7 | 1 |
| Checks_Cleared | REAL | 7 | 1 |
| Checks_Outstanding | REAL | 7 | 1 |
| Deposits_Cleared | REAL | 7 | 1 |
| Deposits_InTransit | REAL | 7 | 1 |
| Other_Cleared | REAL | 7 | 1 |
| Other_Outstanding | REAL | 7 | 1 |
| UnreconciledAmount | REAL | 7 | 1 |
| ServiceChargeAmount | REAL | 7 | 1 |
| SC_AccountNumber | CLOB | 13 | 1 |
| InterestAmount | REAL | 7 | 1 |
| Int_AccountNumber | CLOB | 13 | 1 |
| JournalEntry_ID | INT32 | 11 | 1 |
| EnteredBy | CLOB | 50 | 1 |
| EnteredDate | TIMESTAMP | 19 | 1 |
| ModifiedBy | CLOB | 50 | 1 |
| ModifiedDate | TIMESTAMP | 19 | 1 |
| ReconciledBalance | REAL | 7 | 1 |
| EnteredTime | INTERVAL | 10 | 1 |
| ModifiedTime | INTERVAL | 10 | 1 |
| x27 | CLOB | 2 | 1 |
| PK_UUID | UUID | 0 | 1 |
| FC_Deposits_InTransit | REAL | 7 | 1 |
| FC_Deposits_Cleared | REAL | 7 | 1 |
| FC_UnreconciledAmount | REAL | 7 | 1 |
| FC_ForeignCurrency_ID | INT32 | 11 | 1 |
| FC_Exchange_Rate | REAL | 7 | 1 |
| FC_EndingBookBalance | REAL | 7 | 1 |
| FC_Checks_Outstanding | REAL | 7 | 1 |
| FC_Other_Outstanding | REAL | 7 | 1 |
| FC_Reconciled_Balance | REAL | 7 | 1 |
| FC_EndingBankBalance | REAL | 7 | 1 |
| FC_Other_InTransit | REAL | 7 | 1 |
| Other_InTransit | REAL | 7 | 1 |
| FC_Other_Cleared | REAL | 7 | 1 |
| FC_D_Total_ExchangeDiff | REAL | 7 | 1 |
| FC_D_Total_Adjustment | REAL | 7 | 1 |
| FC_O_Total_ExchangeDiff | REAL | 7 | 1 |
| FC_O_Total_Adjustment | REAL | 7 | 1 |
| AVL_46 | BOOLEAN | 5 | 1 |

### AP_Check_Register

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| AP_BankAccount_ID | INT32 | 11 | 1 |
| BankAccount_Name | CLOB | 30 | 1 |
| CheckNumber | INT32 | 11 | 1 |
| Check_Date | TIMESTAMP | 19 | 1 |
| Check_Amount | REAL | 7 | 1 |
| Check_Payee | CLOB | 80 | 1 |
| PrintedBy | CLOB | 50 | 1 |
| PrintedDate | TIMESTAMP | 19 | 1 |
| VoidedBy | CLOB | 50 | 1 |
| VoidedDate | TIMESTAMP | 19 | 1 |
| Void_GL_PostStatus | CLOB | 10 | 1 |
| SupplierNum | INT32 | 11 | 1 |
| Void_AP_PostStatus | CLOB | 10 | 1 |
| AP_Check_Run_ID | INT32 | 11 | 1 |
| AP_Hand_Check_ID | INT32 | 11 | 1 |
| Void_OriginalPayee | CLOB | 50 | 1 |
| Void_PostToDate | TIMESTAMP | 19 | 1 |
| VoidedTime | INTERVAL | 10 | 1 |
| PrintedTime | INTERVAL | 10 | 1 |
| PK_UUID | UUID | 0 | 1 |

### AP_Check_Run

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| Check_Date | TIMESTAMP | 19 | 1 |
| Description | CLOB | 80 | 1 |
| PostToDate | TIMESTAMP | 19 | 1 |
| FirstCheckNumber | INT32 | 11 | 1 |
| BankAccountName | CLOB | 30 | 1 |
| AP_BankAccount_ID | INT32 | 11 | 1 |
| AcctBalanceB4CheckRun | REAL | 7 | 1 |
| CheckRunAmount | REAL | 7 | 1 |
| AcctBalanceAfterRun | REAL | 7 | 1 |
| CheckRun_Discount | REAL | 7 | 1 |
| AP_PostingStatus | CLOB | 10 | 1 |
| EnteredBy | CLOB | 50 | 1 |
| EnteredDate | TIMESTAMP | 19 | 1 |
| ModifiedBy | CLOB | 50 | 1 |
| ModifiedDate | TIMESTAMP | 19 | 1 |
| PrintedBy | CLOB | 50 | 1 |
| PrintedDate | TIMESTAMP | 19 | 1 |
| CheckReg_PostingStatus | CLOB | 10 | 1 |
| GL_PostingStatus | CLOB | 10 | 1 |
| GL_Detail_ID | INT32 | 11 | 1 |
| GL_Detail_ID_DiscDebit | INT32 | 11 | 1 |
| GL_Detail_ID_DiscCredit | INT32 | 11 | 1 |
| NumberofChecks | INT32 | 11 | 1 |
| LastCheckNumber | INT32 | 11 | 1 |
| EnteredTime | INTERVAL | 10 | 1 |
| ModifiedTime | INTERVAL | 10 | 1 |
| PrintedTime | INTERVAL | 10 | 1 |
| PK_UUID | UUID | 0 | 1 |

### AP_Check_Run_Detail

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| AP_Check_Run_ID | INT32 | 11 | 1 |
| AP_Balance_ID | INT32 | 11 | 1 |
| Check_Amount | REAL | 7 | 1 |
| DiscountTaken | REAL | 7 | 1 |
| CheckNumber | INT32 | 11 | 1 |
| Detail_Status | CLOB | 10 | 1 |
| CheckRegister_ID | INT32 | 11 | 1 |
| Pay | BOOLEAN | 5 | 1 |
| Force | BOOLEAN | 5 | 1 |
| SupplierName | CLOB | 80 | 1 |
| InvoiceNumber | CLOB | 20 | 1 |
| InvoiceDate | TIMESTAMP | 19 | 1 |
| SupplierNum | INT32 | 11 | 1 |
| SupplierNameNumSortKey | CLOB | 60 | 1 |
| AP_Transaction_ID | INT32 | 11 | 1 |
| NewPrepayment | BOOLEAN | 5 | 1 |
| TempCheck_ID | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |

### AP_Check_Run_TempChecks

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| AP_CheckRun_ID | INT32 | 11 | 1 |
| CheckNumber | INT32 | 11 | 1 |
| SupplierName | CLOB | 50 | 1 |
| CheckAmount | REAL | 7 | 1 |
| Printed_OK | BOOLEAN | 5 | 1 |
| VoidAndReprint | BOOLEAN | 5 | 1 |
| PrintAgain | BOOLEAN | 5 | 1 |
| CancelPrinting | BOOLEAN | 5 | 1 |
| StatusIsSet | BOOLEAN | 5 | 1 |
| CheckRegisterStatus | CLOB | 20 | 1 |
| AP_Check_Register_ID | INT32 | 11 | 1 |
| GL_Detail_ID | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |

### AP_Checks_VoidedGL_Lines

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| AP_Check_Register_ID | INT32 | 11 | 1 |
| AccountNum | CLOB | 13 | 1 |
| AcctTypeAbbr | CLOB | 2 | 1 |
| Debit | REAL | 7 | 1 |
| Credit | REAL | 7 | 1 |
| GL_Detail_ID | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |

### AP_Checks_VoidedInfo

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| AP_Check_Register_ID | INT32 | 11 | 1 |
| AP_Balance_ID | INT32 | 11 | 1 |
| Check_Amount | REAL | 7 | 1 |
| Discount_Amount | REAL | 7 | 1 |
| SupplierName | CLOB | 80 | 1 |
| SupplierNumber | INT32 | 11 | 1 |
| AP_Transaction_ID | INT32 | 11 | 1 |
| InvoiceNumber | CLOB | 20 | 1 |
| PK_UUID | UUID | 0 | 1 |

### AP_Constants

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| RecalcAging | BOOLEAN | 5 | 1 |
| Current_Aging_Date | TIMESTAMP | 19 | 1 |
| Current_Aging_Time | INTERVAL | 10 | 1 |
| Current_Aging_AgedBy | CLOB | 20 | 1 |
| Historical_Aging_AsOf | TIMESTAMP | 19 | 1 |
| Historical_Aging_CalcDate | TIMESTAMP | 19 | 1 |
| Historical_Aging_CalcTime | INTERVAL | 10 | 1 |
| Historical_Aging_AgeBy | CLOB | 20 | 1 |
| Col_1_DD_Days | INT32 | 11 | 1 |
| Col_1_DD_Header | CLOB | 20 | 1 |
| Col_1_ID_Days | INT32 | 11 | 1 |
| Col_1_ID_Header | CLOB | 20 | 1 |
| Col_2_DD_Days | INT32 | 11 | 1 |
| Col_2_DD_Header | CLOB | 20 | 1 |
| Col_2_ID_Days | INT32 | 11 | 1 |
| Col_2_ID_Header | CLOB | 20 | 1 |
| Col_3_DD_Days | INT32 | 11 | 1 |
| Col_3_DD_Header | CLOB | 20 | 1 |
| Col_3_ID_Days | INT32 | 11 | 1 |
| Col_3_ID_Header | CLOB | 20 | 1 |
| Col_4_DD_Header | CLOB | 20 | 1 |
| Col_4_ID_Header | CLOB | 20 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### AP_Hand_Checks

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| CheckDate | TIMESTAMP | 19 | 1 |
| CheckNumber | INT32 | 11 | 1 |
| BankAccountName | CLOB | 30 | 1 |
| AP_Bank_Account_ID | INT32 | 11 | 1 |
| CheckAmount | REAL | 7 | 1 |
| DiscountAmount | REAL | 7 | 1 |
| Supplier_ID | INT32 | 11 | 1 |
| Supplier_Name | CLOB | 80 | 1 |
| RemitToAddress | CLOB | 0 | 1 |
| Check_Type | CLOB | 20 | 1 |
| EnteredBy | CLOB | 50 | 1 |
| EnteredDate | TIMESTAMP | 19 | 1 |
| ModifiedBy | CLOB | 50 | 1 |
| ModifiedDate | TIMESTAMP | 19 | 1 |
| AP_PostingStatus | CLOB | 10 | 1 |
| CheckReg_PostingStatus | CLOB | 10 | 1 |
| GL_PostingStatus | CLOB | 10 | 1 |
| GL_Detail_ID | INT32 | 11 | 1 |
| GL_Detail_ID_DiscDebit | INT32 | 11 | 1 |
| GL_Detail_ID_DiscCredit | INT32 | 11 | 1 |
| PostToDate | TIMESTAMP | 19 | 1 |
| Undistributed | REAL | 7 | 1 |
| AP_CheckRegister_ID | INT32 | 11 | 1 |
| EnteredTime | INTERVAL | 10 | 1 |
| ModifiedTime | INTERVAL | 10 | 1 |
| PK_UUID | UUID | 0 | 1 |

### AP_Hand_Checks_AP

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| AP_Hand_Checks_ID | INT32 | 11 | 1 |
| AP_Balance_ID | INT32 | 11 | 1 |
| Check_Amount | REAL | 7 | 1 |
| Discount_Taken | REAL | 7 | 1 |
| Invoice_Date | TIMESTAMP | 19 | 1 |
| Invoice_Number | CLOB | 20 | 1 |
| BalanceDue | REAL | 7 | 1 |
| Invoice_Amount | REAL | 7 | 1 |
| DiscountAvailable | REAL | 7 | 1 |
| SupplierNum | INT32 | 11 | 1 |
| SupplierNameNumSortKey | CLOB | 60 | 1 |
| AP_Transaction_ID | INT32 | 11 | 1 |
| NewPrepayment | BOOLEAN | 5 | 1 |
| Pay | BOOLEAN | 5 | 1 |
| GL_Detail_ID | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |

### AP_Hand_Checks_GL

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| AP_Hand_Checks_ID | INT32 | 11 | 1 |
| AccountNumber | CLOB | 13 | 1 |
| AccountName | CLOB | 40 | 1 |
| AcctTypeAbbr | CLOB | 2 | 1 |
| TicketNumber | CLOB | 12 | 1 |
| Amount | REAL | 7 | 1 |
| GL_Detail_ID | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |

### AP_Invoice

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| Supplier_ID | INT32 | 11 | 1 |
| SupplierName | CLOB | 80 | 1 |
| Invoice_Number | CLOB | 20 | 1 |
| Invoice_Date | TIMESTAMP | 19 | 1 |
| Post_To_Date | TIMESTAMP | 19 | 1 |
| DiscountDays | INT32 | 11 | 1 |
| DiscountPercent | REAL | 7 | 1 |
| NetDaysDue | INT32 | 11 | 1 |
| DiscountDate | TIMESTAMP | 19 | 1 |
| DiscountAmount | REAL | 7 | 1 |
| InvoiceDueDate | TIMESTAMP | 19 | 1 |
| RemitToAddress | CLOB | 0 | 1 |
| PO_ExtendedAmount | REAL | 7 | 1 |
| Invoice_Amount | REAL | 7 | 1 |
| TotalDistributed | REAL | 7 | 1 |
| Undistributed | REAL | 7 | 1 |
| GL_PostStatus | CLOB | 10 | 1 |
| AP_PostingStatus | CLOB | 10 | 1 |
| AP_Transaction_ID | INT32 | 11 | 1 |
| EnteredBy | CLOB | 50 | 1 |
| EnteredDate | TIMESTAMP | 19 | 1 |
| ModifiedBy | CLOB | 50 | 1 |
| ModifiedDate | TIMESTAMP | 19 | 1 |
| FromPO_Number | CLOB | 10 | 1 |
| GL_Detail_ID | INT32 | 11 | 1 |
| Notes | CLOB | 0 | 1 |
| EnteredTime | INTERVAL | 10 | 1 |
| ModifiedTime | INTERVAL | 10 | 1 |
| TaxRegionID | INT32 | 11 | 1 |
| TaxRegionRate | REAL | 7 | 1 |
| Tax | REAL | 7 | 1 |
| TicketNum | CLOB | 12 | 1 |
| BatchReceiptID | INT32 | 11 | 1 |
| Currency_ID | INT32 | 11 | 1 |
| Currency_ExchangeRate | REAL | 7 | 1 |
| FCT_PO_ExtAmount | REAL | 7 | 1 |
| FCT_InvoiceAmount | REAL | 7 | 1 |
| NetDaysDue_EOM | BOOLEAN | 5 | 1 |
| DiscountDays_EOM | BOOLEAN | 5 | 1 |
| Currency_Rate_ID | INT32 | 11 | 1 |
| Mex_Comprobante | INT16 | 6 | 1 |
| Mex_UUID_Serie | CLOB | 36 | 1 |
| PK_UUID | UUID | 0 | 1 |
| paymentType | CLOB | 45 | 1 |
| Tag | CLOB | 3 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### AP_Invoice_Line

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| AP_Invoice_ID | INT32 | 11 | 1 |
| AccountNumber | CLOB | 13 | 1 |
| AccountName | CLOB | 40 | 1 |
| AccountTypeAbbr | CLOB | 2 | 1 |
| PO_Number | CLOB | 10 | 1 |
| TicketNumber | CLOB | 12 | 1 |
| Amount | REAL | 7 | 1 |
| GL_Detail_ID | INT32 | 11 | 1 |
| PO_ReceiptBatchID | INT32 | 11 | 1 |
| TaxOnPurchaseAccount | BOOLEAN | 5 | 1 |
| x12 | CLOB | 0 | 1 |
| x13 | CLOB | 0 | 1 |
| x14 | CLOB | 0 | 1 |
| x15 | CLOB | 0 | 1 |
| x16 | CLOB | 0 | 1 |
| x17 | CLOB | 0 | 1 |
| x18 | CLOB | 0 | 1 |
| x19 | CLOB | 0 | 1 |
| x20 | CLOB | 0 | 1 |
| x21 | CLOB | 0 | 1 |
| x22 | CLOB | 0 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### AP_Invoice_Tax

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| AP_Invoice_ID | INT32 | 11 | 1 |
| Ship_Country | CLOB | 25 | 1 |
| Ship_State | CLOB | 25 | 1 |
| Region_Country | CLOB | 25 | 1 |
| Region_State | CLOB | 25 | 1 |
| Region_ID | INT32 | 11 | 1 |
| Region_Name | CLOB | 80 | 1 |
| TaxType_ID | INT32 | 11 | 1 |
| TaxType_Name | CLOB | 80 | 1 |
| TaxType_Rate | REAL | 7 | 1 |
| TotalSaleAmount | REAL | 7 | 1 |
| TaxableAmount | REAL | 7 | 1 |
| NonTaxableAmt | REAL | 7 | 1 |
| ExemptAmount | REAL | 7 | 1 |
| AP_Invoice_Line_ID | INT32 | 11 | 1 |
| Post_To_Date | TIMESTAMP | 19 | 1 |
| TotalAmountSubjectToTax | REAL | 7 | 1 |
| TaxType_Country | CLOB | 25 | 1 |
| TaxType_State | CLOB | 25 | 1 |
| TaxAmount | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |

### AP_Maint_ApplyTo_AP

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| AP_Maintenance_ID | INT32 | 11 | 1 |
| Supplier_ID | INT32 | 11 | 1 |
| Supplier_Name | CLOB | 80 | 1 |
| AP_Balance_ID | INT32 | 11 | 1 |
| Invoice_Number | CLOB | 20 | 1 |
| Invoice_Date | TIMESTAMP | 19 | 1 |
| InvoiceAmount | REAL | 7 | 1 |
| BalDue_B4Maintenance | REAL | 7 | 1 |
| AP_Transaction_ID | INT32 | 11 | 1 |
| DebitAmount | REAL | 7 | 1 |
| CreditAmount | REAL | 7 | 1 |
| InvoiceDueDate | TIMESTAMP | 19 | 1 |
| InvoiceDiscountAmount | REAL | 7 | 1 |
| RemainingDue | REAL | 7 | 1 |
| Pay | BOOLEAN | 5 | 1 |
| NewPrepayment | BOOLEAN | 5 | 1 |
| BalDue_After_Maintenance | REAL | 7 | 1 |
| FCT_InvoiceAmount | REAL | 7 | 1 |
| FCT_BalDue_B4_Maint | REAL | 7 | 1 |
| FCT_BalDue_AfterMaint | REAL | 7 | 1 |
| FCT_DebitAmount | REAL | 7 | 1 |
| FCT_CreditAmount | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |

### AP_Maint_ApplyTo_GL

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| AP_Maintenance_ID | INT32 | 11 | 1 |
| AccountNumber | CLOB | 13 | 1 |
| AccountName | CLOB | 40 | 1 |
| AccountTypeAbbr | CLOB | 2 | 1 |
| TicketNumber | CLOB | 12 | 1 |
| Amount | REAL | 7 | 1 |
| GL_Detail_ID | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |

### AP_Maintenance

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| Supplier_ID | INT32 | 11 | 1 |
| Supplier_Name | CLOB | 80 | 1 |
| Invoice_Number | CLOB | 20 | 1 |
| AP_Balance_ID | INT32 | 11 | 1 |
| Invoice_Date | TIMESTAMP | 19 | 1 |
| AP_Transaction_ID | INT32 | 11 | 1 |
| AP_Maint_Type | CLOB | 20 | 1 |
| AP_PostingStatus | CLOB | 20 | 1 |
| Debit_Amount | REAL | 7 | 1 |
| CreditAmount | REAL | 7 | 1 |
| PostToDate | TIMESTAMP | 19 | 1 |
| o_AP_Invoice_ID | INT32 | 11 | 1 |
| Bal_Due_After_Adjust | REAL | 7 | 1 |
| InvoiceBalanceDue | REAL | 7 | 1 |
| InvoiceOriginalAmtDue | REAL | 7 | 1 |
| GL_PostingStatus | CLOB | 30 | 1 |
| InvoiceDueDate | TIMESTAMP | 19 | 1 |
| EnteredBy | CLOB | 50 | 1 |
| EnteredDate | TIMESTAMP | 19 | 1 |
| ModifiedBy | CLOB | 50 | 1 |
| ModifiedDate | TIMESTAMP | 19 | 1 |
| MaintenanceNote | CLOB | 0 | 1 |
| DistributedAmt | REAL | 7 | 1 |
| Undistributed | REAL | 7 | 1 |
| GL_Detail_ID | INT32 | 11 | 1 |
| TotalDiscount | REAL | 7 | 1 |
| EnteredTime | INTERVAL | 10 | 1 |
| ModifiedTime | INTERVAL | 10 | 1 |
| Currency_ID | INT32 | 11 | 1 |
| Currency_ExchangeRate | REAL | 7 | 1 |
| FCT_DebitAmount | REAL | 7 | 1 |
| FCT_CreditAmount | REAL | 7 | 1 |
| FCT_InvoiceBalDue | REAL | 7 | 1 |
| FCT_BalDueAfterAdjust | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |
| glPrefix | CLOB | 3 | 1 |

### AP_Transaction

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| AP_Balance_ID | INT32 | 11 | 1 |
| Invoice_Number | CLOB | 20 | 1 |
| TransactionType | CLOB | 20 | 1 |
| TransactionAmount | REAL | 7 | 1 |
| TransactionDate | TIMESTAMP | 19 | 1 |
| PostToDate | TIMESTAMP | 19 | 1 |
| SourceDocumentKey | CLOB | 50 | 1 |
| FCT_TransactionAmt | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### AR_Aging_CustCollectNotes

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| Customer_ID | CLOB | 10 | 1 |
| Notes | CLOB | 0 | 1 |
| PK_UUID | UUID | 0 | 1 |

### AR_Aging_Customer

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| Customer_ID | CLOB | 10 | 1 |
| BalanceDue | REAL | 7 | 1 |
| Aging_Current | REAL | 7 | 1 |
| Aging_Over30 | REAL | 7 | 1 |
| Aging_Over60 | REAL | 7 | 1 |
| Aging_Over90 | REAL | 7 | 1 |
| CustomerName | CLOB | 80 | 1 |
| PK_UUID | UUID | 0 | 1 |

### AR_Aging_Customer_Historical

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| Customer_ID | CLOB | 10 | 1 |
| CustomerNAme | CLOB | 40 | 1 |
| BalanceDue | REAL | 7 | 1 |
| Aging_Current | REAL | 7 | 1 |
| Aging_Over30 | REAL | 7 | 1 |
| Aging_Over60 | REAL | 7 | 1 |
| Aging_Over90 | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |

### AR_Aging_Invoice

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| Invoice_ID | INT32 | 11 | 1 |
| AR_Balance_ID | INT32 | 11 | 1 |
| Customer_ID | CLOB | 10 | 1 |
| BalanceDue | REAL | 7 | 1 |
| Aging_Current | REAL | 7 | 1 |
| Aging_Over30 | REAL | 7 | 1 |
| Aging_Over60 | REAL | 7 | 1 |
| Aging_Over90 | REAL | 7 | 1 |
| CustomerName | CLOB | 40 | 1 |
| SalesRep_Number | CLOB | 10 | 1 |
| Invoice_Date | TIMESTAMP | 19 | 1 |
| CustomerNameNumKey | CLOB | 50 | 1 |
| MFG_Rep_ID | CLOB | 10 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### AR_Aging_Invoice_Historical

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| Invoice_ID | INT32 | 11 | 1 |
| AR_Balance_ID | INT32 | 11 | 1 |
| Customer_ID | CLOB | 10 | 1 |
| CustomerName | CLOB | 40 | 1 |
| BalanceDue | REAL | 7 | 1 |
| Aging_Current | REAL | 7 | 1 |
| Aging_Over30 | REAL | 7 | 1 |
| Aging_Over60 | REAL | 7 | 1 |
| Aging_Over90 | REAL | 7 | 1 |
| Invoice_Date | TIMESTAMP | 19 | 1 |
| CustomerNameNumKey | CLOB | 50 | 1 |
| FCT_BalanceDue | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |

### AR_Balance

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| Invoice_ID | INT32 | 11 | 1 |
| Invoice_Date | TIMESTAMP | 19 | 1 |
| DueDate | TIMESTAMP | 19 | 1 |
| Customer_ID | CLOB | 10 | 1 |
| Customer_Name | CLOB | 80 | 1 |
| OriginalAmountDue | REAL | 7 | 1 |
| BalanceDue | REAL | 7 | 1 |
| DiscountAmount | REAL | 7 | 1 |
| Ticket_ID | CLOB | 10 | 1 |
| SalesRep_Number | CLOB | 10 | 1 |
| Source | CLOB | 20 | 1 |
| IncludeInAverageDaysPaid | CLOB | 3 | 1 |
| CustomerNameNumKey | CLOB | 50 | 1 |
| DatePaidOff | TIMESTAMP | 19 | 1 |
| FCT_OriginalAmtDue | REAL | 7 | 1 |
| FCT_BalanceDue | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |
| glPrefix | CLOB | 3 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |

### AR_Balance_FAT

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| AR_Balance_ID | INT32 | 11 | 1 |
| Notes | CLOB | 0 | 1 |
| PK_UUID | UUID | 0 | 1 |

### AR_CreditCardAccounts

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| CardName | CLOB | 20 | 1 |
| FeePercent | REAL | 7 | 1 |
| FeeGL_AcctNum | CLOB | 13 | 1 |
| FeeGL_AcctName | CLOB | 40 | 1 |
| Inactive | BOOLEAN | 5 | 1 |
| PK_UUID | UUID | 0 | 1 |

### AR_Maint_ApplyTo_AR

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| AR_Maintenance_ID | INT32 | 11 | 1 |
| Customer_ID | CLOB | 10 | 1 |
| Customer_Name | CLOB | 80 | 1 |
| AR_Balance_ID | INT32 | 11 | 1 |
| Invoice_ID | INT32 | 11 | 1 |
| Invoice_Date | TIMESTAMP | 19 | 1 |
| InvoiceAmount | REAL | 7 | 1 |
| BalDue_B4Maintenance | REAL | 7 | 1 |
| AR_Transaction_ID | INT32 | 11 | 1 |
| DebitAmount | REAL | 7 | 1 |
| CreditAmount | REAL | 7 | 1 |
| InvoiceDueDate | TIMESTAMP | 19 | 1 |
| InvoiceDiscountAmount | REAL | 7 | 1 |
| BalDue_After_Maintenance | REAL | 7 | 1 |
| FCT_InvoiceAmount | REAL | 7 | 1 |
| FCT_BalDue_B4_Maint | REAL | 7 | 1 |
| FCT_BalDue_AfterMaint | REAL | 7 | 1 |
| FCT_DebitAmount | REAL | 7 | 1 |
| FCT_CreditAmount | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |

### AR_Maint_ApplyTo_GL

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| AR_Maintenance_ID | INT32 | 11 | 1 |
| AccountNumber | CLOB | 13 | 1 |
| AccountName | CLOB | 40 | 1 |
| AccountTypeAbbr | CLOB | 2 | 1 |
| TicketNumber | CLOB | 12 | 1 |
| Amount | REAL | 7 | 1 |
| GL_Detail_ID | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |

### AR_Maintenance

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| Customer_ID | CLOB | 10 | 1 |
| Customer_Name | CLOB | 80 | 1 |
| Invoice_ID | INT32 | 11 | 1 |
| AR_Balance_ID | INT32 | 11 | 1 |
| Invoice_Date | TIMESTAMP | 19 | 1 |
| AR_Transaction_ID | INT32 | 11 | 1 |
| AR_Maint_Type | CLOB | 20 | 1 |
| AR_PostingStatus | CLOB | 30 | 1 |
| Debit_Amount | REAL | 7 | 1 |
| Credit_Amount | REAL | 7 | 1 |
| PostToDate | TIMESTAMP | 19 | 1 |
| Ticket_ID | CLOB | 10 | 1 |
| Bal_Due_After_Adjust | REAL | 7 | 1 |
| InvoiceBalanceDue | REAL | 7 | 1 |
| InvoiceOriginalAmtDue | REAL | 7 | 1 |
| AVL_Not_Used | CLOB | 0 | 1 |
| InvoiceDueDate | TIMESTAMP | 19 | 1 |
| EnteredBy | CLOB | 50 | 1 |
| EnteredDate | TIMESTAMP | 19 | 1 |
| ModifiedBy | CLOB | 50 | 1 |
| ModifiedDate | TIMESTAMP | 19 | 1 |
| MaintenanceNote | CLOB | 0 | 1 |
| DistributedAmt | REAL | 7 | 1 |
| Undistributed | REAL | 7 | 1 |
| GL_PostingStatus | CLOB | 10 | 1 |
| GL_Detail_ID | INT32 | 11 | 1 |
| EnteredTime | INTERVAL | 10 | 1 |
| ModifiedTime | INTERVAL | 10 | 1 |
| Currency_ID | INT32 | 11 | 1 |
| Currency_ExchangeRate | REAL | 7 | 1 |
| FCT_DebitAmount | REAL | 7 | 1 |
| FCT_CreditAmount | REAL | 7 | 1 |
| FCT_InvoiceBalDue | REAL | 7 | 1 |
| FCT_BalDueAfterAdjust | REAL | 7 | 1 |
| Currency_Rate_ID | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |
| glPrefix | CLOB | 3 | 1 |

### AR_Transaction

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| AR_Balance_ID | INT32 | 11 | 1 |
| Invoice_ID | INT32 | 11 | 1 |
| TransactionType | CLOB | 20 | 1 |
| TransactionAmount | REAL | 7 | 1 |
| TransactionDate | TIMESTAMP | 19 | 1 |
| PostToDate | TIMESTAMP | 19 | 1 |
| SourceDocumentKey | CLOB | 50 | 1 |
| FCT_TransactionAmt | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### AccountingForms

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| Current_Aging_Date | TIMESTAMP | 19 | 1 |
| Current_Aging_Time | INTERVAL | 10 | 1 |
| Current_AgedBy | CLOB | 20 | 1 |
| Historical_AgedAsOf | TIMESTAMP | 19 | 1 |
| Historical_Calculated_Date | TIMESTAMP | 19 | 1 |
| Historical_Calculated_Time | INTERVAL | 10 | 1 |
| Historical_Age_By | CLOB | 20 | 1 |
| Col_1_DD_Days | INT32 | 11 | 1 |
| Col_1_DD_Header | CLOB | 20 | 1 |
| Col_1_ID_Days | INT32 | 11 | 1 |
| Col_1_ID_Header | CLOB | 20 | 1 |
| Col_2_DD_Days | INT32 | 11 | 1 |
| Col_2_DD_Header | CLOB | 20 | 1 |
| Col_2_ID_Days | INT32 | 11 | 1 |
| Col_2_ID_Header | CLOB | 20 | 1 |
| Col_3_DD_Days | INT32 | 11 | 1 |
| Col_3_DD_Header | CLOB | 20 | 1 |
| Col_3_ID_Days | INT32 | 11 | 1 |
| Col_3_ID_Header | CLOB | 20 | 1 |
| Col_4_DD_Header | CLOB | 20 | 1 |
| Col_4_ID_Header | CLOB | 20 | 1 |
| Current_RecalcAging | BOOLEAN | 5 | 1 |
| Historical_RecalcAging | BOOLEAN | 5 | 1 |
| PK_UUID | UUID | 0 | 1 |

### Active4D

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| PK_UUID | UUID | 0 | 1 |

### Activity

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| ActDate | TIMESTAMP | 19 | 1 |
| AssociateNum | CLOB | 10 | 1 |
| Associate | CLOB | 60 | 1 |
| Notes | CLOB | 0 | 1 |
| CustomerNum | CLOB | 10 | 1 |
| ActType | CLOB | 80 | 1 |
| RBCallBack | INT16 | 6 | 1 |
| NextCallDate | TIMESTAMP | 19 | 1 |
| Contact | CLOB | 40 | 1 |
| Priority | CLOB | 15 | 1 |
| Addr1 | CLOB | 255 | 1 |
| Addr2 | CLOB | 255 | 1 |
| City | CLOB | 40 | 1 |
| State_Province | CLOB | 25 | 1 |
| Zip | CLOB | 15 | 1 |
| Country | CLOB | 25 | 1 |
| Phone | CLOB | 20 | 1 |
| Fax | CLOB | 20 | 1 |
| Extension | CLOB | 10 | 1 |
| Email | CLOB | 60 | 1 |
| Dept | CLOB | 25 | 1 |
| Pager | CLOB | 20 | 1 |
| Cell | CLOB | 20 | 1 |
| ProdGroup | CLOB | 40 | 1 |
| Contact_ID | CLOB | 10 | 1 |
| Collection_Customer_ID | CLOB | 10 | 1 |
| Letter_ | BLOB | 0 | 1 |
| EnteredBy | CLOB | 50 | 1 |
| ModifiedBy | CLOB | 50 | 1 |
| EnteredDate | TIMESTAMP | 19 | 1 |
| ModifiedDate | TIMESTAMP | 19 | 1 |
| EnteredTime | INTERVAL | 10 | 1 |
| ModifiedTime | INTERVAL | 10 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### Address

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| Classification | CLOB | 20 | 1 |
| Location | CLOB | 80 | 1 |
| Addr1 | CLOB | 255 | 1 |
| Addr2 | CLOB | 255 | 1 |
| City | CLOB | 40 | 1 |
| State_Province | CLOB | 25 | 1 |
| County | CLOB | 20 | 1 |
| Zip | CLOB | 15 | 1 |
| CustNumber | CLOB | 10 | 1 |
| Country | CLOB | 25 | 1 |
| EntryBy | CLOB | 50 | 1 |
| EntryDate | TIMESTAMP | 19 | 1 |
| ModifyBy | CLOB | 50 | 1 |
| ModifyDate | TIMESTAMP | 19 | 1 |
| SendToA4 | CLOB | 20 | 1 |
| A4LinkDate | TIMESTAMP | 19 | 1 |
| A4ShipToID | INT32 | 11 | 1 |
| A4ClientID | INT32 | 11 | 1 |
| Web_Site | CLOB | 80 | 1 |
| Phone | CLOB | 20 | 1 |
| Ship_Instructions | CLOB | 50 | 1 |
| Ship_Attention | CLOB | 30 | 1 |
| SalesTax_RegionID | INT32 | 11 | 1 |
| TaxExemptCertificate | CLOB | 40 | 1 |
| TaxExemptCert_PrintOnInv | BOOLEAN | 5 | 1 |
| TaxExemptCertExpire | TIMESTAMP | 19 | 1 |
| TaxExempt_SalesTax | BOOLEAN | 5 | 1 |
| TaxExemptCert_Resale | BOOLEAN | 5 | 1 |
| TaxExemptOverrideCustomerRec | BOOLEAN | 5 | 1 |
| EntryTime | INTERVAL | 10 | 1 |
| ModifyTime | INTERVAL | 10 | 1 |
| ShipVia | CLOB | 40 | 1 |
| Freight_AcctNo | CLOB | 20 | 1 |
| RotometricsShipToAddrID | CLOB | 20 | 1 |
| RotoMetricsBillToAddrID | CLOB | 20 | 1 |
| eCommShipToID | CLOB | 25 | 1 |
| Classification_Local | CLOB | 255 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### Affiliate

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| CompanyName | CLOB | 40 | 1 |
| SerialNumber | CLOB | 20 | 1 |
| Password | CLOB | 20 | 1 |
| PK_UUID | UUID | 0 | 1 |
| Created_Date | TIMESTAMP | 19 | 1 |
| Created_Time | INTERVAL | 10 | 1 |
| Created_Employee_ID | CLOB | 10 | 1 |
| Created_Employee_Name | CLOB | 50 | 1 |
| Modified_Employee_Name | CLOB | 50 | 1 |
| Modified_Date | TIMESTAMP | 19 | 1 |
| Modified_Time | INTERVAL | 10 | 1 |
| Modified_Employee_ID | CLOB | 10 | 1 |

### Associate

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| Number | CLOB | 10 | 1 |
| FirstName | CLOB | 15 | 1 |
| MidInitial | CLOB | 2 | 1 |
| LastName | CLOB | 35 | 1 |
| Addr1 | CLOB | 255 | 1 |
| Addr2 | CLOB | 255 | 1 |
| City | CLOB | 40 | 1 |
| State_Province | CLOB | 25 | 1 |
| Zip | CLOB | 15 | 1 |
| Phone | CLOB | 20 | 1 |
| Deprecated_1 | CLOB | 20 | 1 |
| StartDate | TIMESTAMP | 19 | 1 |
| EndDate | TIMESTAMP | 19 | 1 |
| Dept | CLOB | 20 | 1 |
| Birthday | CLOB | 10 | 1 |
| Anniversary | CLOB | 10 | 1 |
| AllotedVacation | REAL | 7 | 1 |
| AllotedHoliday | REAL | 7 | 1 |
| AllotedPersonal | REAL | 7 | 1 |
| TotVacation | REAL | 7 | 1 |
| TotHoliday | REAL | 7 | 1 |
| TotalPersonal | REAL | 7 | 1 |
| Mug | BLOB | 0 | 1 |
| Notes | CLOB | 0 | 1 |
| EmergContact | CLOB | 45 | 1 |
| EmergPhone | CLOB | 20 | 1 |
| Password | CLOB | 254 | 1 |
| Group_Unused | CLOB | 20 | 1 |
| CustomerEdit | BOOLEAN | 5 | 1 |
| AllotedSick | REAL | 7 | 1 |
| TotalSick | REAL | 7 | 1 |
| ProspectBtn | INT32 | 11 | 1 |
| CustomerBtn | INT32 | 11 | 1 |
| MFGRepsBtn | INT32 | 11 | 1 |
| EstimateBtn | INT32 | 11 | 1 |
| StockBtn | INT32 | 11 | 1 |
| EquipmentBtn | INT32 | 11 | 1 |
| ToolPricingBtn | INT32 | 11 | 1 |
| ToolingBtn | INT32 | 11 | 1 |
| KnowledgeBtn | INT32 | 11 | 1 |
| SupplierBtn | INT32 | 11 | 1 |
| AssociatesBtn | INT32 | 11 | 1 |
| ConstantsBtn | BOOLEAN | 5 | 1 |
| ProductsBtn | INT32 | 11 | 1 |
| TicketsBtn | INT32 | 11 | 1 |
| PackingSlipBtn | INT32 | 11 | 1 |
| InventoryBtn | INT32 | 11 | 1 |
| PurchaseBtn | INT32 | 11 | 1 |
| TicketStatBtn | INT32 | 11 | 1 |
| POStatBtn | INT32 | 11 | 1 |
| InvoicesBtn | INT32 | 11 | 1 |
| CashReceiptsBtn | INT32 | 11 | 1 |
| TimeCardsBtn | INT32 | 11 | 1 |
| StockProductsBtn | INT32 | 11 | 1 |
| SwitchUserBtn | BOOLEAN | 5 | 1 |
| PassWordBtn | BOOLEAN | 5 | 1 |
| AdditionalReports_Access | BOOLEAN | 5 | 1 |
| AddNewCustomer_Access | BOOLEAN | 5 | 1 |
| CustCreditApproval_Access | BOOLEAN | 5 | 1 |
| ConvertProspToCust_Access | BOOLEAN | 5 | 1 |
| QuickReport_Access | BOOLEAN | 5 | 1 |
| AccountingReports_Access | BOOLEAN | 5 | 1 |
| CustomerReports_Access | BOOLEAN | 5 | 1 |
| StockReports_Access | BOOLEAN | 5 | 1 |
| TickettReports_Access | BOOLEAN | 5 | 1 |
| TimeCardReports_Access | BOOLEAN | 5 | 1 |
| AllowDelete_Access | BOOLEAN | 5 | 1 |
| EditPopUp_Access | BOOLEAN | 5 | 1 |
| EditSuperReport_Access | BOOLEAN | 5 | 1 |
| ManageStockProduct_Access | BOOLEAN | 5 | 1 |
| CustomExport_Access | BOOLEAN | 5 | 1 |
| RebuildTikEst_v_Act_Access | BOOLEAN | 5 | 1 |
| StockInventory_Access | INT32 | 11 | 1 |
| AccountingDelete_Access | BOOLEAN | 5 | 1 |
| AccountingReissue_Access | BOOLEAN | 5 | 1 |
| FC_Affiliates_Btn | INT32 | 11 | 1 |
| FC_Projects_Btn | INT32 | 11 | 1 |
| WebServer_Control_Btn | BOOLEAN | 5 | 1 |
| GetTonerUsage_Btn | BOOLEAN | 5 | 1 |
| PressTimeClock_Access | BOOLEAN | 5 | 1 |
| FinishTimeClock_Access | BOOLEAN | 5 | 1 |
| EditSchedule_Access | BOOLEAN | 5 | 1 |
| AR_Aging_Btn | INT32 | 11 | 1 |
| AR_Maintenance_Btn | INT32 | 11 | 1 |
| AccountingConstants_Btn | INT32 | 11 | 1 |
| ChartOfAccounts_Btn | INT32 | 11 | 1 |
| StockProdEstimatesBtn | INT32 | 11 | 1 |
| StockProdTicketsBtn | INT32 | 11 | 1 |
| StockProdTikStatsBtn | BOOLEAN | 5 | 1 |
| JournalEntryBtn | INT32 | 11 | 1 |
| OverrideSoftClose_Access | BOOLEAN | 5 | 1 |
| FinancialStatementBtn | INT32 | 11 | 1 |
| Dash_Display_Btn | BOOLEAN | 5 | 1 |
| API_Btn | INT32 | 11 | 1 |
| AP_InvoiceBtn | INT32 | 11 | 1 |
| OfficePhoneExtension | CLOB | 20 | 1 |
| AP_AgingBtn | BOOLEAN | 5 | 1 |
| AP_Maintenance_Btn | INT32 | 11 | 1 |
| AP_PrintChecksBtn | INT32 | 11 | 1 |
| AP_HandChecksBtn | INT32 | 11 | 1 |
| AP_CheckRegisterBtn | INT32 | 11 | 1 |
| Display_Tool_Tips | BOOLEAN | 5 | 1 |
| E_Mail_Address | CLOB | 80 | 1 |
| AP_BankReconciliationBtn | BOOLEAN | 5 | 1 |
| Access_4D_Write | BOOLEAN | 5 | 1 |
| Edit_4D_Write | BOOLEAN | 5 | 1 |
| ModifyAP_DueDates | BOOLEAN | 5 | 1 |
| ModifyAR_DueDates | BOOLEAN | 5 | 1 |
| Quality_Procedures_Btn | INT32 | 11 | 1 |
| Return_Materials_Btn | INT32 | 11 | 1 |
| NonConform_Materials_Btn | INT32 | 11 | 1 |
| Complaint_Log_Btn | INT32 | 11 | 1 |
| Documentation_Btn | INT32 | 11 | 1 |
| Edit_PhraseList | BOOLEAN | 5 | 1 |
| Commissions_Btn | INT32 | 11 | 1 |
| CannotEditSecurity | BOOLEAN | 5 | 1 |
| BudgetingNotes | CLOB | 0 | 1 |
| ExecutiveTrends_Btn | INT32 | 11 | 1 |
| IncludeInOutBoard | BOOLEAN | 5 | 1 |
| ViewInOutBoard | BOOLEAN | 5 | 1 |
| AdminInOutBoard | BOOLEAN | 5 | 1 |
| Rate_Class | INT32 | 11 | 1 |
| ABC_Btn | INT32 | 11 | 1 |
| EstPriceTunerPage | BOOLEAN | 5 | 1 |
| SMTP_Auth_UserName | CLOB | 40 | 1 |
| SMTP_Auth_Password | CLOB | 254 | 1 |
| Edit_Inactive | BOOLEAN | 5 | 1 |
| Hide_Commission | BOOLEAN | 5 | 1 |
| GL_Analysis_Btn | INT32 | 11 | 1 |
| AccessAnyEstimate | BOOLEAN | 5 | 1 |
| Language_Btn | INT32 | 11 | 1 |
| LanguageChoice | INT32 | 11 | 1 |
| SalesTax_AccessToTaxSetUp | BOOLEAN | 5 | 1 |
| SalesTax_Btn | INT32 | 11 | 1 |
| Access_RemoveTiksToInv | BOOLEAN | 5 | 1 |
| Access_ReverseInvoices | BOOLEAN | 5 | 1 |
| UEF_Btn | INT32 | 11 | 1 |
| eTraxxLog_Btn | BOOLEAN | 5 | 1 |
| Product_Is_GroupUpdateOn | BOOLEAN | 5 | 1 |
| Country | CLOB | 25 | 1 |
| DeDuplication_Btn | BOOLEAN | 5 | 1 |
| GL_Budgets_Btn | INT32 | 11 | 1 |
| Edit_TicketBillings | BOOLEAN | 5 | 1 |
| Edit_ExchangeRates | BOOLEAN | 5 | 1 |
| PDF_Email_Report_Access | BOOLEAN | 5 | 1 |
| eTraxxConstants_Btn | BOOLEAN | 5 | 1 |
| Cust_Restrict_AR_Reports | BOOLEAN | 5 | 1 |
| Cust_Lock_Budgets_Tab | BOOLEAN | 5 | 1 |
| Cust_Restrict_AR_Tabs | BOOLEAN | 5 | 1 |
| ESC_Art | BOOLEAN | 5 | 1 |
| ESC_Proof | BOOLEAN | 5 | 1 |
| ESC_Plate | BOOLEAN | 5 | 1 |
| ESC_Tool | BOOLEAN | 5 | 1 |
| ESC_Ink | BOOLEAN | 5 | 1 |
| ESC_Stock | BOOLEAN | 5 | 1 |
| ESC_Press | BOOLEAN | 5 | 1 |
| ESC_Equip | BOOLEAN | 5 | 1 |
| ESC_Finish | BOOLEAN | 5 | 1 |
| ESC_Ship | BOOLEAN | 5 | 1 |
| ESC_TickStat | BOOLEAN | 5 | 1 |
| ESC_On | BOOLEAN | 5 | 1 |
| ESS_Ship | BOOLEAN | 5 | 1 |
| ESS_TickStat | BOOLEAN | 5 | 1 |
| ESS_On | BOOLEAN | 5 | 1 |
| Address_Add_Btn | BOOLEAN | 5 | 1 |
| Address_Class_Unlimited | BOOLEAN | 5 | 1 |
| Address_Edit_SalesTax | BOOLEAN | 5 | 1 |
| ElectronicPayments_Btn | INT32 | 11 | 1 |
| Are_TimeCardPasswordsRequired | BOOLEAN | 5 | 1 |
| SupplierTab_Accounting | BOOLEAN | 5 | 1 |
| SupplierTab_InvHist | BOOLEAN | 5 | 1 |
| SupplierTab_AP_Bal | BOOLEAN | 5 | 1 |
| SupplierTab_eCommerce | BOOLEAN | 5 | 1 |
| SupplierTab_Activity | BOOLEAN | 5 | 1 |
| SupplierTab_POs | BOOLEAN | 5 | 1 |
| SupplierTab_Inventory | BOOLEAN | 5 | 1 |
| PressMetricsReport | BOOLEAN | 5 | 1 |
| ReceiveStockAtTimeClock | BOOLEAN | 5 | 1 |
| ViewRestrictedSuppliers | BOOLEAN | 5 | 1 |
| ViewTicketEstvAct | BOOLEAN | 5 | 1 |
| StockProductsReports | BOOLEAN | 5 | 1 |
| CommissionPercent | REAL | 7 | 1 |
| TimeClock_Btn | BOOLEAN | 5 | 1 |
| UnlockEstimates | BOOLEAN | 5 | 1 |
| JDF_Diagnostics | BOOLEAN | 5 | 1 |
| JDF_Constants | BOOLEAN | 5 | 1 |
| AssignGLDistProduct | BOOLEAN | 5 | 1 |
| Edit_TicketCommonPage | BOOLEAN | 5 | 1 |
| Send_Ticket_JDF | BOOLEAN | 5 | 1 |
| Remove_Ticket_JDF | BOOLEAN | 5 | 1 |
| ESC_Equip3 | BOOLEAN | 5 | 1 |
| ESC_Equip4 | BOOLEAN | 5 | 1 |
| AssignBOMs | BOOLEAN | 5 | 1 |
| EntryBy | CLOB | 50 | 1 |
| ModifiedBy | CLOB | 50 | 1 |
| EntryDate | TIMESTAMP | 19 | 1 |
| ModifiedDate | TIMESTAMP | 19 | 1 |
| EntryTime | INTERVAL | 10 | 1 |
| ModifiedTime | INTERVAL | 10 | 1 |
| eTraxxPrefs_x | BLOB | 0 | 1 |
| Web_Enable_Login | BOOLEAN | 5 | 1 |
| SchedTicketStatus_Btn | BOOLEAN | 5 | 1 |
| SchedEmployeeStatus_Btn | BOOLEAN | 5 | 1 |
| MultiSchedule_Btn | BOOLEAN | 5 | 1 |
| SchedProductPrepressStatus_Btn | BOOLEAN | 5 | 1 |
| SchedCapacityPlanning_Btn | BOOLEAN | 5 | 1 |
| SchedAdvancedVisual_Btn | INT32 | 11 | 1 |
| ServerAdminWindow | BOOLEAN | 5 | 1 |
| Foreign_Currencies_Btn | INT32 | 11 | 1 |
| Estimate_Permitted_Forms | INT32 | 11 | 1 |
| Inactive | BOOLEAN | 5 | 1 |
| Allow_MultipleDeletion | BOOLEAN | 5 | 1 |
| Allow_MultiDupe | BOOLEAN | 5 | 1 |
| ExternalDoc_Btn | INT32 | 11 | 1 |
| Inspection_Btn | BOOLEAN | 5 | 1 |
| CompleteAll_Btn | BOOLEAN | 5 | 1 |
| PK_UUID | UUID | 0 | 1 |
| Dash_Goal_Display_Btn | BOOLEAN | 5 | 1 |
| Product_Permitted_Forms | INT32 | 11 | 1 |
| Ticket_Permitted_Forms | INT32 | 11 | 1 |
| Password_Expiration_date | TIMESTAMP | 19 | 1 |
| Password_user_set | BOOLEAN | 5 | 1 |
| Password_Encrypted | BOOLEAN | 5 | 1 |
| iPodTouch_Btn | BOOLEAN | 5 | 1 |
| IMAP_sentFolderName | CLOB | 255 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |
| Tag | CLOB | 3 | 1 |
| multiLocationID | CLOB | 0 | 1 |
| BatchedPS_Btn | INT32 | 11 | 1 |
| CompleteAll_PO_Btn | BOOLEAN | 5 | 1 |
| ESC_Equip5 | BOOLEAN | 5 | 1 |
| ESC_Equip6 | BOOLEAN | 5 | 1 |
| Misc_Info | CLOB | 20 | 1 |
| EntStockProduct_Btn | BOOLEAN | 5 | 1 |
| workShift | CLOB | 20 | 1 |
| AutoLoadAllRecords | BOOLEAN | 5 | 1 |
| InventoryReports_Access | BOOLEAN | 5 | 1 |
| AnalysisReports_Access | BOOLEAN | 5 | 1 |
| EmployeesReports_Access | BOOLEAN | 5 | 1 |

### BB_Misc

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 80 | 1 |
| Alpha1 | CLOB | 80 | 1 |
| Alpha2 | CLOB | 80 | 1 |
| Alpha3 | CLOB | 80 | 1 |
| Alpha4 | CLOB | 80 | 1 |
| Text1 | CLOB | 0 | 1 |
| Time1 | INTERVAL | 10 | 1 |
| Date1 | TIMESTAMP | 19 | 1 |
| Longint1 | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |

### Banks_list

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| Primary_key | INT32 | 11 | 1 |
| Code | CLOB | 3 | 1 |
| Short_Name | CLOB | 40 | 1 |
| Long_name | CLOB | 100 | 1 |
| Routing_num | CLOB | 20 | 1 |
| Other_country | BOOLEAN | 5 | 1 |
| NU_2 | BOOLEAN | 5 | 1 |
| NU_3 | BOOLEAN | 5 | 1 |
| NU_4 | BOOLEAN | 5 | 1 |
| NU_5 | BOOLEAN | 5 | 1 |
| PK_UUID | UUID | 0 | 1 |

### Blob_Chunk

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| Chunk_Number | INT32 | 11 | 1 |
| Total_Chunks | INT32 | 11 | 1 |
| Creation_UTC | CLOB | 80 | 1 |
| Creation_DateTime | INT32 | 11 | 1 |
| Blob_Object | BLOB | 0 | 1 |
| PK_UUID | UUID | 0 | 1 |

### Budget_AssociateSales

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| Associate_ID | CLOB | 10 | 1 |
| AcctYear_ID | INT32 | 11 | 1 |
| AcctYear_Month | INT32 | 11 | 1 |
| MonthEndDate | TIMESTAMP | 19 | 1 |
| Month_Name | CLOB | 10 | 1 |
| BudgetedSales | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |

### Budget_CustomerSales

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| Customer_ID | CLOB | 10 | 1 |
| Associate_ID | CLOB | 10 | 1 |
| AcctYear_ID | INT32 | 11 | 1 |
| AcctYear_Month | INT32 | 11 | 1 |
| MonthEndDate | TIMESTAMP | 19 | 1 |
| Month_Name | CLOB | 10 | 1 |
| BudgetedSales | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |
| updateTimeDateStamp | CLOB | 255 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |

### CDF_Definition

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |
| TableName | CLOB | 30 | 1 |
| QL_Record_Type | CLOB | 255 | 1 |
| Label | CLOB | 50 | 1 |
| Field_Type | CLOB | 20 | 1 |
| OrderToView | INT16 | 6 | 1 |
| isRequired | BOOLEAN | 5 | 1 |
| Notes | CLOB | 0 | 1 |
| Inactive | BOOLEAN | 5 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |
| EnteredBy | CLOB | 50 | 1 |
| EnteredDate | TIMESTAMP | 19 | 1 |
| EnteredTime | INTERVAL | 10 | 1 |
| ModifiedBy | CLOB | 50 | 1 |
| ModifiedDate | TIMESTAMP | 19 | 1 |
| ModifiedTime | INTERVAL | 10 | 1 |
| Tag | CLOB | 3 | 1 |

### CDF_ListValues

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |
| CDF_Definition_ID | INT32 | 11 | 1 |
| CDF_Value | CLOB | 255 | 1 |

### CDF_Values

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |
| CDF_Definition_ID | INT32 | 11 | 1 |
| TableName | CLOB | 15 | 1 |
| Table_Key_ID | CLOB | 15 | 1 |
| Field_Type | CLOB | 20 | 1 |
| Text_Value | CLOB | 0 | 1 |
| Date_Value | TIMESTAMP | 19 | 1 |
| Boolean_Value | BOOLEAN | 5 | 1 |
| Integer_Value | INT32 | 11 | 1 |
| Real_Value | REAL | 7 | 1 |
| Time_Value | INTERVAL | 10 | 1 |
| List_Value | CLOB | 255 | 1 |
| EnteredBy | CLOB | 255 | 1 |
| EnteredDate | TIMESTAMP | 19 | 1 |
| EnteredTime | INTERVAL | 10 | 1 |
| ModifiedBy | CLOB | 255 | 1 |
| ModifiedDate | TIMESTAMP | 19 | 1 |
| ModifiedTime | INTERVAL | 10 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |
| QL_Record_Type | CLOB | 255 | 1 |
| Inactive | BOOLEAN | 5 | 1 |

### CRON_Event_Log

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| Job_ID | CLOB | 10 | 1 |
| Job_Name | CLOB | 40 | 1 |
| DateTimeStamp | CLOB | 40 | 1 |
| Event | CLOB | 80 | 1 |
| Event_Message | CLOB | 255 | 1 |
| Event_Date | TIMESTAMP | 19 | 1 |
| Event_Time | INTERVAL | 10 | 1 |
| Method | CLOB | 40 | 1 |
| AVL_F10 | BOOLEAN | 5 | 1 |
| PK_UUID | UUID | 0 | 1 |

### CRON_Job

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| Name | CLOB | 80 | 1 |
| Method | CLOB | 40 | 1 |
| Parameter_List | CLOB | 40 | 1 |
| Is_Enabled | BOOLEAN | 5 | 1 |
| Run_At_Time | INTERVAL | 10 | 1 |
| Is_Run_Once | BOOLEAN | 5 | 1 |
| Run_Once_Date | TIMESTAMP | 19 | 1 |
| AVL_F9 | BOOLEAN | 5 | 1 |
| AVL_F10 | BOOLEAN | 5 | 1 |
| AVL_F11 | BOOLEAN | 5 | 1 |
| PK_UUID | UUID | 0 | 1 |

### CR_ApplyTo_AR

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| CR_Checks_ID | INT32 | 11 | 1 |
| Invoice_ID | INT32 | 11 | 1 |
| AmountReceived | REAL | 7 | 1 |
| DiscountApplied | REAL | 7 | 1 |
| InvoiceAmount | REAL | 7 | 1 |
| BalDue_B4Payment | REAL | 7 | 1 |
| AR_Transaction_ID | INT32 | 11 | 1 |
| AR_Balance_ID | INT32 | 11 | 1 |
| BalDue_AfterPayment | REAL | 7 | 1 |
| DateReceivedApplied | TIMESTAMP | 19 | 1 |
| AmountSubjectToCommission | REAL | 7 | 1 |
| CommissionPercentage | REAL | 7 | 1 |
| TotalCommissionAmount | REAL | 7 | 1 |
| Customer_ID | CLOB | 10 | 1 |
| CustomerName | CLOB | 80 | 1 |
| SalesRep_ID | CLOB | 10 | 1 |
| SalesRep_Name | CLOB | 50 | 1 |
| ModifiedBy | CLOB | 50 | 1 |
| ModifiedDate | TIMESTAMP | 19 | 1 |
| CommissionThisReceipt | REAL | 7 | 1 |
| DaysToPay | INT32 | 11 | 1 |
| MFG_Rep_ID | CLOB | 10 | 1 |
| MFG_Rep_Name | CLOB | 80 | 1 |
| MFG_Rep_Comm_Rate | REAL | 7 | 1 |
| MFG_Rep_SubjectToComm | REAL | 7 | 1 |
| MFG_Rep_CommThisReceipt | REAL | 7 | 1 |
| MFG_Rep_TotalComm | REAL | 7 | 1 |
| CommissionPaid | BOOLEAN | 5 | 1 |
| Notes | CLOB | 0 | 1 |
| Invoice_Date | TIMESTAMP | 19 | 1 |
| ExcludePlateColorChange | BOOLEAN | 5 | 1 |
| ModifiedTime | INTERVAL | 10 | 1 |
| TicketNumber | CLOB | 12 | 1 |
| FCT_CurrencyAdjust | REAL | 7 | 1 |
| FCT_InvoiceAmount | REAL | 7 | 1 |
| FCT_BalDue_B4Payment | REAL | 7 | 1 |
| FCT_BalDue_AfterPayment | REAL | 7 | 1 |
| FCT_AmountReceived | REAL | 7 | 1 |
| FCT_DiscountApplied | REAL | 7 | 1 |
| TakeDiscount_CB | BOOLEAN | 5 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### CR_ApplyTo_GL

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| CR_Checks_ID | INT32 | 11 | 1 |
| AccountNumber | CLOB | 13 | 1 |
| AccountName | CLOB | 40 | 1 |
| AccountTypeAbbr | CLOB | 2 | 1 |
| TicketNumber | CLOB | 12 | 1 |
| Amount | REAL | 7 | 1 |
| GL_Detail_ID | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### CR_Checks

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| CR_Deposit_ID | INT32 | 11 | 1 |
| Customer_ID | CLOB | 10 | 1 |
| Customer_Name | CLOB | 80 | 1 |
| Check_Number | CLOB | 30 | 1 |
| Check_Amount | REAL | 7 | 1 |
| Deposit_Type | CLOB | 20 | 1 |
| EnteredBy | CLOB | 50 | 1 |
| EnteredDate | TIMESTAMP | 19 | 1 |
| ModifiedBy | CLOB | 50 | 1 |
| ModifiedDate | TIMESTAMP | 19 | 1 |
| MiscCR_Notes | CLOB | 80 | 1 |
| MiscCR_ReceivedFrom | CLOB | 80 | 1 |
| AR_Transaction_ID | INT32 | 11 | 1 |
| Invoice_ID | CLOB | 10 | 1 |
| DistributedAmt | REAL | 7 | 1 |
| Undistributed | REAL | 7 | 1 |
| CC_Account_ID | INT32 | 11 | 1 |
| CC_Card_Name | CLOB | 20 | 1 |
| CC_Fee_Percent | REAL | 7 | 1 |
| CC_Fee_Dollars | REAL | 7 | 1 |
| Deposit_method_index | INT16 | 6 | 1 |
| EnteredTime | INTERVAL | 10 | 1 |
| ModifiedTime | INTERVAL | 10 | 1 |
| Currency_ID | INT32 | 11 | 1 |
| Currency_ExchangeRate | REAL | 7 | 1 |
| BankFees | REAL | 7 | 1 |
| FCT_BankFees | REAL | 7 | 1 |
| FCT_CheckAmount | REAL | 7 | 1 |
| GL_Detail_ID_CurrAdj | INT32 | 11 | 1 |
| GL_Detail_ID_CurrAdj_AR | INT32 | 11 | 1 |
| Currency_Rate_ID | INT32 | 11 | 1 |
| Deposit_method_text | CLOB | 255 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### CR_Deposit

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| DepositDate | TIMESTAMP | 19 | 1 |
| BankAccount | CLOB | 30 | 1 |
| PostToDate | TIMESTAMP | 19 | 1 |
| DepositTotal | REAL | 7 | 1 |
| EnteredBy | CLOB | 50 | 1 |
| EnteredDate | TIMESTAMP | 19 | 1 |
| ModifiedBy | CLOB | 50 | 1 |
| ModifiedDate | TIMESTAMP | 19 | 1 |
| AR_PostingStatus | CLOB | 20 | 1 |
| GL_PostingStatus | CLOB | 10 | 1 |
| GL_Detail_ID_CashDebit | INT32 | 11 | 1 |
| GL_Detail_ID_AR_Credit | INT32 | 11 | 1 |
| GL_Detail_ID_DiscountDebit | INT32 | 11 | 1 |
| CC_Fee_Total | REAL | 7 | 1 |
| CC_Fee_GL_AcctNum | CLOB | 13 | 1 |
| GL_Detail_ID_CC_Fees | INT32 | 11 | 1 |
| EnteredTime | INTERVAL | 10 | 1 |
| ModifiedTime | INTERVAL | 10 | 1 |
| AVL_x_notused | CLOB | 0 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### Constants

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| Company | CLOB | 80 | 1 |
| Addr1 | CLOB | 255 | 1 |
| Addr2 | CLOB | 255 | 1 |
| City | CLOB | 40 | 1 |
| State_Province | CLOB | 25 | 1 |
| Zip | CLOB | 15 | 1 |
| EstLetterMsg | CLOB | 0 | 1 |
| OverRun | REAL | 7 | 1 |
| SlitRewindSet | BOOLEAN | 5 | 1 |
| MultiLayout | BOOLEAN | 5 | 1 |
| ModDate | TIMESTAMP | 19 | 1 |
| PlateMaterial | REAL | 7 | 1 |
| StepCharge | REAL | 7 | 1 |
| DistortCharge | REAL | 7 | 1 |
| PlateSetUp | REAL | 7 | 1 |
| PlateMarkUp | REAL | 7 | 1 |
| Steel1Descr | CLOB | 10 | 1 |
| Steel1Price | REAL | 7 | 1 |
| Steel2Descr | CLOB | 10 | 1 |
| Steel2Price | REAL | 7 | 1 |
| Steel3Descr | CLOB | 10 | 1 |
| Steel3Price | REAL | 7 | 1 |
| ChromePercent | REAL | 7 | 1 |
| ToolMarkup | REAL | 7 | 1 |
| WrapQuant1 | INT16 | 6 | 1 |
| WrapCost1 | REAL | 7 | 1 |
| WrapQuant2 | INT16 | 6 | 1 |
| WrapCost2 | REAL | 7 | 1 |
| FinishGrossRate | REAL | 7 | 1 |
| WrapCost3 | REAL | 7 | 1 |
| MSIPerPound | REAL | 7 | 1 |
| WeightPerCtn | REAL | 7 | 1 |
| CartonCost | REAL | 7 | 1 |
| PoundsPerHr | REAL | 7 | 1 |
| FinishNetRate | REAL | 7 | 1 |
| CoreCost | REAL | 7 | 1 |
| Patch_Date | TIMESTAMP | 19 | 1 |
| TaxFreight | BOOLEAN | 5 | 1 |
| ArtMarkup | REAL | 7 | 1 |
| StockMarkup | REAL | 7 | 1 |
| SubbedMarkUp | REAL | 7 | 1 |
| ULinkFact | REAL | 7 | 1 |
| ULAdminFee | REAL | 7 | 1 |
| Margin | REAL | 7 | 1 |
| ToolShipCharge | REAL | 7 | 1 |
| HandFanFold | INT16 | 6 | 1 |
| StockAddWidth | REAL | 7 | 1 |
| MinPackCost | REAL | 7 | 1 |
| PressCylindSz1 | REAL | 7 | 1 |
| PressCylindSz2 | REAL | 7 | 1 |
| PressCylindSz3 | REAL | 7 | 1 |
| PrinterPaper_A4_Default | BOOLEAN | 5 | 1 |
| Are_Ship_Instructions_to_Print | BOOLEAN | 5 | 1 |
| LockProfitMargi | BOOLEAN | 5 | 1 |
| ModTime | INTERVAL | 10 | 1 |
| LogoBMP | BLOB | 0 | 1 |
| DistribBMP | BLOB | 0 | 1 |
| PckLetterMsg | CLOB | 0 | 1 |
| DefPSAddr | BOOLEAN | 5 | 1 |
| Country | CLOB | 25 | 1 |
| Schedule_IsPrepOnlyIncluded | BOOLEAN | 5 | 1 |
| UseAllPressesForNumberOfPlates | BOOLEAN | 5 | 1 |
| API_Is_StckPrd_ImageTransfer | BOOLEAN | 5 | 1 |
| Currency_Symbol | CLOB | 5 | 1 |
| Currency_Is_In_Front | BOOLEAN | 5 | 1 |
| Negative_Currency_Format | BOOLEAN | 5 | 1 |
| Decimal_PlaceHolder | CLOB | 3 | 1 |
| Thousands_Separator | CLOB | 3 | 1 |
| Negative_Number_Format | BOOLEAN | 5 | 1 |
| LanguageTitle_1 | CLOB | 40 | 1 |
| LanguageTitle_2 | CLOB | 40 | 1 |
| LanguageTitle_3 | CLOB | 40 | 1 |
| LanguageTitle_4 | CLOB | 40 | 1 |
| LanguageTitle_5 | CLOB | 40 | 1 |
| LanguageTitle_6 | CLOB | 40 | 1 |
| LanguageTitle_7 | CLOB | 40 | 1 |
| ToolShape_Pinfeed | CLOB | 40 | 1 |
| ToolShape_Rectangle | CLOB | 40 | 1 |
| ToolShape_PrintCylinder | CLOB | 40 | 1 |
| ToolShape_WilsonPunch | CLOB | 40 | 1 |
| Add_Freight_to_Estimate | BOOLEAN | 5 | 1 |
| Freight_Markup_Rate | REAL | 7 | 1 |
| Estimate_PriceMode_Default | CLOB | 20 | 1 |
| Is_SPInventory_Allowed_Neg | BOOLEAN | 5 | 1 |
| ToolShape_MagneticCylinder | CLOB | 40 | 1 |
| CustTicket_Allow_LineItem_Dupe | BOOLEAN | 5 | 1 |
| StockTicket_AllowLineItemDupe | BOOLEAN | 5 | 1 |
| PackSlip_Default_ShipClass | CLOB | 10 | 1 |
| UK_RotoMetric_ToolPrices | BOOLEAN | 5 | 1 |
| NumericFormat_Country | CLOB | 20 | 1 |
| LangFont_ALP_Win | CLOB | 40 | 1 |
| ToolShape_FlatbedGear | CLOB | 40 | 1 |
| Is_Kit_Inventory_Calculated | BOOLEAN | 5 | 1 |
| EmailAttachmentEncoding | INT32 | 11 | 1 |
| Email_SMTP_PortNumber | INT32 | 11 | 1 |
| CC_PO_Gen_PN | CLOB | 20 | 1 |
| CC_PO_Gen_PID | INT32 | 11 | 1 |
| CC_Misc_PN | CLOB | 20 | 1 |
| CC_Misc_PID | INT32 | 11 | 1 |
| CC_Freight_PN | CLOB | 20 | 1 |
| CC_Freight_PID | INT32 | 11 | 1 |
| CD_Subtotal_PN | CLOB | 20 | 1 |
| CD_Subtot_PID | INT32 | 11 | 1 |
| CD_PlateCng_PN | CLOB | 20 | 1 |
| CD_PlateC_PID | INT32 | 11 | 1 |
| CD_ColorCng_PN | CLOB | 20 | 1 |
| CD_ColorC_PID | INT32 | 11 | 1 |
| CD_PO_Art_PN | CLOB | 20 | 1 |
| CD_PO_Art_PID | INT32 | 11 | 1 |
| CD_PO_Plate_PN | CLOB | 20 | 1 |
| CD_PO_Plate_PID | INT32 | 11 | 1 |
| CD_PO_Tool_PN | CLOB | 20 | 1 |
| CD_PO_Tool_PID | INT32 | 11 | 1 |
| CD_PO_Gen_PN | CLOB | 20 | 1 |
| CD_PO_Gen_PID | INT32 | 11 | 1 |
| CD_Misc_PN | CLOB | 20 | 1 |
| CD_Misc_PID | INT32 | 11 | 1 |
| CD_Freight_PN | CLOB | 20 | 1 |
| CD_Freight_PID | INT32 | 11 | 1 |
| SPI_Subtotal_PN | CLOB | 20 | 1 |
| SPI_Subtot_PID | INT32 | 11 | 1 |
| SPI_Misc_PN | CLOB | 20 | 1 |
| SPI_Misc_PID | INT32 | 11 | 1 |
| SPI_Freight_PN | CLOB | 20 | 1 |
| SPI_Freight_PID | INT32 | 11 | 1 |
| SPC_Subtotal_PN | CLOB | 20 | 1 |
| SPC_Subtot_PID | INT32 | 11 | 1 |
| SPC_Misc_PN | CLOB | 20 | 1 |
| SPC_Misc_PID | INT32 | 11 | 1 |
| SPC_Freight_PN | CLOB | 20 | 1 |
| SPC_Freight_PID | INT32 | 11 | 1 |
| SPD_Subtotal_PN | CLOB | 20 | 1 |
| SPD_Subtot_PID | INT32 | 11 | 1 |
| SPD_Misc_PN | CLOB | 20 | 1 |
| SPD_Misc_PID | INT32 | 11 | 1 |
| SPD_Freight_PN | CLOB | 20 | 1 |
| SPD_Freight_PID | INT32 | 11 | 1 |
| A4ConvDate | TIMESTAMP | 19 | 1 |
| Is_UseV9Interface | BOOLEAN | 5 | 1 |
| A4_Win_NC_Name | CLOB | 40 | 1 |
| A4_AR_Aging_Nam | CLOB | 30 | 1 |
| A4_SalesTax_Nam | CLOB | 30 | 1 |
| FlexPackEst_PriceMode_Default | CLOB | 20 | 1 |
| AvailSchHrs_Art | REAL | 7 | 1 |
| AvailSchHrs_Prf | REAL | 7 | 1 |
| AvailSchHrs_Plt | REAL | 7 | 1 |
| AvailSchHrs_Tol | REAL | 7 | 1 |
| AvailSchHrs_FF | REAL | 7 | 1 |
| AvailSchHrs_Pck | REAL | 7 | 1 |
| AvailSchHrs_Stk | REAL | 7 | 1 |
| eTraxx_Is_StckPrd_ImageTransfr | BOOLEAN | 5 | 1 |
| AvailSchHrs_Ink | REAL | 7 | 1 |
| AvailSchHrs_Mai | REAL | 7 | 1 |
| ProdName1Descr | CLOB | 20 | 1 |
| ProdName2Descr | CLOB | 20 | 1 |
| ProdName3Descr | CLOB | 20 | 1 |
| ProdName4Descr | CLOB | 20 | 1 |
| ProdPopUp1Descr | CLOB | 20 | 1 |
| ProdPopUp2Descr | CLOB | 20 | 1 |
| eTraxx_Is_CstmPrd_ImageTransfr | BOOLEAN | 5 | 1 |
| eTraxx_TransferPath | CLOB | 0 | 1 |
| Century_PivotYear | INT32 | 11 | 1 |
| API_Is_CstmPrd_ImageTransfer | BOOLEAN | 5 | 1 |
| API_TransferPath | CLOB | 0 | 1 |
| PostInvoicesToLT_AR | TIMESTAMP | 19 | 1 |
| Tax_ID | CLOB | 40 | 1 |
| SMTP_Host_Name | CLOB | 80 | 1 |
| CreditLimitOverridePW | CLOB | 20 | 1 |
| InvoiceSpoilageJobs | BOOLEAN | 5 | 1 |
| Sched_OnTime_Color | CLOB | 20 | 1 |
| Sched_OnTime_Style | CLOB | 20 | 1 |
| Sched_NearDue_Color | CLOB | 20 | 1 |
| Sched_NearDue_Style | CLOB | 20 | 1 |
| Sched_Late_Color | CLOB | 20 | 1 |
| Sched_Late_Style | CLOB | 20 | 1 |
| NearDue_Days | INT32 | 11 | 1 |
| Sched_ScheduledColor | CLOB | 20 | 1 |
| Sched_ScheduledStyle | CLOB | 20 | 1 |
| Sched_StartColor | CLOB | 20 | 1 |
| Sched_StartStyle | CLOB | 20 | 1 |
| Sched_EndColor | CLOB | 20 | 1 |
| Sched_EndStyle | CLOB | 20 | 1 |
| Sched_HoldColor | CLOB | 20 | 1 |
| Sched_HoldStyle | CLOB | 20 | 1 |
| StartShift_RoundType | CLOB | 20 | 1 |
| StartShift_RoundPeriod | CLOB | 20 | 1 |
| EndShift_RoundType | CLOB | 20 | 1 |
| EndShift_RoundPeriod | CLOB | 20 | 1 |
| Log_Errors | BOOLEAN | 5 | 1 |
| InOutBoardRefreshRate | CLOB | 30 | 1 |
| Web_Email_Template | CLOB | 0 | 1 |
| PackSlip_PrintWarnings | BOOLEAN | 5 | 1 |
| ABC_Minimum_Time | CLOB | 30 | 1 |
| ABC_Minimum_Cost | CLOB | 30 | 1 |
| ABC_Maximum_Time | CLOB | 30 | 1 |
| TimeZoneCode | CLOB | 4 | 1 |
| ObservesDaylightSavingsTime | BOOLEAN | 5 | 1 |
| OfficePhone | CLOB | 20 | 1 |
| OfficeFax | CLOB | 20 | 1 |
| Location | CLOB | 20 | 1 |
| SMTP_Auth_Mode | CLOB | 20 | 1 |
| Ticket_Allow_EndUser_Customer | BOOLEAN | 5 | 1 |
| ExcludePlateColorFromComms | BOOLEAN | 5 | 1 |
| ModUser | CLOB | 0 | 1 |
| ipAddress | CLOB | 40 | 1 |
| JDF_StartJDF_Date | TIMESTAMP | 19 | 1 |
| JDF_OnlyTicketsWithArtPlate | BOOLEAN | 5 | 1 |
| JDF_MachineName | CLOB | 80 | 1 |
| NoProductFromEstMsg | BOOLEAN | 5 | 1 |
| ForeignCurrencyFactor | REAL | 7 | 1 |
| AddressType | CLOB | 0 | 1 |
| ToolChooserTolerance | REAL | 7 | 1 |
| SPL_InvoiceCustomTicket | BOOLEAN | 5 | 1 |
| CustName1Descr | CLOB | 20 | 1 |
| CustName2Descr | CLOB | 20 | 1 |
| CustName3Descr | CLOB | 20 | 1 |
| CustName4Descr | CLOB | 20 | 1 |
| CustPopUp1Descr | CLOB | 20 | 1 |
| CustPopUp2Descr | CLOB | 20 | 1 |
| CustCB1Descr | CLOB | 20 | 1 |
| CustCB2Descr | CLOB | 20 | 1 |
| ShrinkSleeve_Overlap_Default | INT32 | 11 | 1 |
| Default_CreditLimit | REAL | 7 | 1 |
| Default_CoreSize | REAL | 7 | 1 |
| ForeignCurrencyFacto_Show | BOOLEAN | 5 | 1 |
| Currency_Abbreviation | CLOB | 5 | 1 |
| Currency_Name | CLOB | 40 | 1 |
| AR_Aging_DefaultAgeByDate | CLOB | 20 | 1 |
| ForeignCurrencyInAP | BOOLEAN | 5 | 1 |
| DoNotCopy_EstPrice_to_Products | BOOLEAN | 5 | 1 |
| Is_InkCoverage_TotalPercent | BOOLEAN | 5 | 1 |
| Are_TimeCardPasswordsRequired | BOOLEAN | 5 | 1 |
| SageCurrencyCode | CLOB | 2 | 1 |
| StockTicket_DupPOs | BOOLEAN | 5 | 1 |
| FiscalYearEndMonthNum | INT32 | 11 | 1 |
| RotoElec_Estimate | BOOLEAN | 5 | 1 |
| RotoElec_PO | BOOLEAN | 5 | 1 |
| RotometricsShipToAddrID | CLOB | 20 | 1 |
| RotoPassword | CLOB | 20 | 1 |
| RotoMetricsBillToAddrID | CLOB | 20 | 1 |
| Is_24_Hour_TimeFormat | BOOLEAN | 5 | 1 |
| UPSS_IP_1 | CLOB | 3 | 1 |
| UPSS_IP_2 | CLOB | 3 | 1 |
| UPSS_IP_3 | CLOB | 3 | 1 |
| UPSS_IP_4 | CLOB | 3 | 1 |
| UPSS_IP_Port | CLOB | 4 | 1 |
| UPSS_UseUPSS | BOOLEAN | 5 | 1 |
| InOutBoardRefreshRate_Local | CLOB | 0 | 1 |
| PackSlip_Override_Worldship | BOOLEAN | 5 | 1 |
| JobCost_Is_PO_Tax_excluded | BOOLEAN | 5 | 1 |
| Regimen_Fiscal | CLOB | 255 | 1 |
| Language_Num_Text | CLOB | 255 | 1 |
| EXT_FileSizeLimit | REAL | 7 | 1 |
| Patch_Date_Client | TIMESTAMP | 19 | 1 |
| PK_UUID | UUID | 0 | 1 |
| EXT_FolderInUse | BOOLEAN | 5 | 1 |
| Email_SendMode | INT16 | 6 | 1 |
| SMTP_Time_out | INT32 | 11 | 1 |
| Email_protocol | INT32 | 11 | 1 |
| Password_min_length | INT16 | 6 | 1 |
| Password_expires | BOOLEAN | 5 | 1 |
| Password_expires_in | INT16 | 6 | 1 |
| Password_req_up_low_case | BOOLEAN | 5 | 1 |
| Password_include_numbers | BOOLEAN | 5 | 1 |
| Password_include_sp_char | BOOLEAN | 5 | 1 |
| Password_sp_char | CLOB | 20 | 1 |
| Password_Reset_All | BOOLEAN | 5 | 1 |
| Password_Temporary | CLOB | 255 | 1 |
| Password_Activate | BOOLEAN | 5 | 1 |
| HP_JobsKey | CLOB | 0 | 1 |
| HP_JobsSecret | CLOB | 0 | 1 |
| HP_JobsURL | CLOB | 0 | 1 |
| HP_startMarker | INT32 | 11 | 1 |
| Password_notice_text | CLOB | 0 | 1 |
| Password_notice | BOOLEAN | 5 | 1 |
| Ticket_UpdatePressEquip | BOOLEAN | 5 | 1 |
| NetworkSleepDisconnect | REAL | 7 | 1 |
| IMAP_hostName | CLOB | 255 | 1 |
| IMAP_portNumber | INT32 | 11 | 1 |
| IMAP_timeOut | INT32 | 11 | 1 |
| IMAP_authenticationMode | CLOB | 255 | 1 |
| SMTP_acceptUnsecureConnection | BOOLEAN | 5 | 1 |
| IMAP_acceptUnsecureConnection | BOOLEAN | 5 | 1 |
| restrictProductNumberChars | BOOLEAN | 5 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |
| Est_Duration | INT32 | 11 | 1 |
| Est_LifespanEnable | BOOLEAN | 5 | 1 |
| emailType | CLOB | 30 | 1 |
| emailProviderClientID | CLOB | 255 | 1 |
| emailProviderSecret | CLOB | 255 | 1 |
| PackSlip_UPS_URL | CLOB | 0 | 1 |
| PackSlip_FedEx_URL | CLOB | 0 | 1 |
| LogoInCustomer | BOOLEAN | 5 | 1 |
| odbcRestricted | CLOB | 0 | 1 |

### Contact

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| CustomerNum | CLOB | 10 | 1 |
| Honorific_Prefix | CLOB | 10 | 1 |
| FirstName | CLOB | 20 | 1 |
| LastName | CLOB | 20 | 1 |
| Title | CLOB | 20 | 1 |
| Phone | CLOB | 20 | 1 |
| Dept | CLOB | 25 | 1 |
| Extension | CLOB | 10 | 1 |
| Patched | TIMESTAMP | 19 | 1 |
| FAX | CLOB | 20 | 1 |
| PerInterests | CLOB | 30 | 1 |
| AddressID | CLOB | 10 | 1 |
| Location | CLOB | 80 | 1 |
| Email | CLOB | 60 | 1 |
| Pager | CLOB | 20 | 1 |
| Cell | CLOB | 20 | 1 |
| AR_Collection_Contact | BOOLEAN | 5 | 1 |
| SendTo_Litho | CLOB | 20 | 1 |
| Litho_LinkDate | TIMESTAMP | 19 | 1 |
| Cust_Serv_No | CLOB | 10 | 1 |
| Sales_Rep_No | CLOB | 10 | 1 |
| ITSName | CLOB | 60 | 1 |
| OTSName | CLOB | 60 | 1 |
| TaxFreight | BOOLEAN | 5 | 1 |
| EnteredBy | CLOB | 50 | 1 |
| ModifyBy | CLOB | 50 | 1 |
| EnteredDate | TIMESTAMP | 19 | 1 |
| ModifyDate | TIMESTAMP | 19 | 1 |
| EnteredTime | INTERVAL | 10 | 1 |
| ModifyTime | INTERVAL | 10 | 1 |
| Web_Enable_Login | BOOLEAN | 5 | 1 |
| Web_Password | CLOB | 20 | 1 |
| eTraxxPrefs_x | BLOB | 0 | 1 |
| eTraxx_Tik_StartDate | TIMESTAMP | 19 | 1 |
| eTraxx_Tik_StopDate | TIMESTAMP | 19 | 1 |
| eTraxx_Tik_DateStore | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### Customer

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| Number | CLOB | 10 | 1 |
| Company | CLOB | 80 | 1 |
| Source | CLOB | 20 | 1 |
| OrderReq | CLOB | 80 | 1 |
| CreditStatus | BOOLEAN | 5 | 1 |
| DistributorNum | CLOB | 10 | 1 |
| MFGRepNum | CLOB | 10 | 1 |
| Notes | CLOB | 0 | 1 |
| Phone | CLOB | 20 | 1 |
| Fax | CLOB | 20 | 1 |
| NextCallDate | TIMESTAMP | 19 | 1 |
| Sales_Rep_No | CLOB | 10 | 1 |
| Cust_Serv_No | CLOB | 10 | 1 |
| SICNum | CLOB | 6 | 1 |
| Customer | BOOLEAN | 5 | 1 |
| Distributor | BOOLEAN | 5 | 1 |
| Receptionist | CLOB | 80 | 1 |
| LastEstimateDat | TIMESTAMP | 19 | 1 |
| TotalEstimates | INT32 | 11 | 1 |
| LastTicketDate | TIMESTAMP | 19 | 1 |
| TotalTickets | INT32 | 11 | 1 |
| TotalSales | REAL | 7 | 1 |
| TotalYTDSales | REAL | 7 | 1 |
| Web_Password | CLOB | 20 | 1 |
| Web_Enable_Login | BOOLEAN | 5 | 1 |
| Days90 | REAL | 7 | 1 |
| TaxExempt_SalesTax | BOOLEAN | 5 | 1 |
| TaxRate | REAL | 7 | 1 |
| DateOpened | TIMESTAMP | 19 | 1 |
| AveDaysPaid | INT16 | 6 | 1 |
| CurrentBalance | REAL | 7 | 1 |
| Terms | CLOB | 45 | 1 |
| TotalLYSales | REAL | 7 | 1 |
| OTSName | CLOB | 35 | 1 |
| ITSName | CLOB | 35 | 1 |
| Prosp_Customer | BOOLEAN | 5 | 1 |
| MFGRepComm | REAL | 7 | 1 |
| DistribName | CLOB | 30 | 1 |
| ZipCode | CLOB | 15 | 1 |
| Territory | CLOB | 2 | 1 |
| Area | CLOB | 2 | 1 |
| StockProdDiscnt | REAL | 7 | 1 |
| StockPrdPriceGp | CLOB | 40 | 1 |
| TaxRate2 | REAL | 7 | 1 |
| Patched | TIMESTAMP | 19 | 1 |
| EntryDate | TIMESTAMP | 19 | 1 |
| EntryBy | CLOB | 50 | 1 |
| ModifyDate | TIMESTAMP | 19 | 1 |
| ModifyBy | CLOB | 50 | 1 |
| A4LinkDate | TIMESTAMP | 19 | 1 |
| SendToA4 | CLOB | 20 | 1 |
| Inactive | BOOLEAN | 5 | 1 |
| URL | CLOB | 0 | 1 |
| Converted_to_Customer | TIMESTAMP | 19 | 1 |
| ProfitAdjLabel | CLOB | 20 | 1 |
| SendStatement | BOOLEAN | 5 | 1 |
| TaxExemptCertificate | CLOB | 40 | 1 |
| Credit_Limit | REAL | 7 | 1 |
| BudgetingNotes | CLOB | 0 | 1 |
| Internal_Customer | BOOLEAN | 5 | 1 |
| SoldToEndUser | BOOLEAN | 5 | 1 |
| Web_Edit_Password | CLOB | 20 | 1 |
| DontPrintTermsOnPS | BOOLEAN | 5 | 1 |
| Overrun_YesNo | INT16 | 6 | 1 |
| Overrun_Amt | REAL | 7 | 1 |
| AutoOrder_StockProduct | INT32 | 11 | 1 |
| TexExemptCertExpire | TIMESTAMP | 19 | 1 |
| TaxExemptCert_Resale | BOOLEAN | 5 | 1 |
| TaxExemptCert_PrintOnInv | BOOLEAN | 5 | 1 |
| eTraxxPrefs_x | BLOB | 0 | 1 |
| EntryTime | INTERVAL | 10 | 1 |
| ModifyTime | INTERVAL | 10 | 1 |
| Type_of_Customer | CLOB | 30 | 1 |
| Name1 | CLOB | 80 | 1 |
| Name2 | CLOB | 80 | 1 |
| Name3 | CLOB | 80 | 1 |
| Name4 | CLOB | 80 | 1 |
| PopUpName1 | CLOB | 40 | 1 |
| PopUpName2 | CLOB | 40 | 1 |
| CheckBoxName1 | BOOLEAN | 5 | 1 |
| CheckBoxName2 | BOOLEAN | 5 | 1 |
| MarketingNotes | CLOB | 0 | 1 |
| TraxxLink_PackSlip_Processing | INT32 | 11 | 1 |
| Currency_ID | INT32 | 11 | 1 |
| StatementAddressID | CLOB | 10 | 1 |
| Web_AllowContactLogIn | BOOLEAN | 5 | 1 |
| CommissionPercent | REAL | 7 | 1 |
| UseEmployeeCommRate | BOOLEAN | 5 | 1 |
| BackStage_ColorStrategy | CLOB | 40 | 1 |
| BackStage_DefaultReportForm | CLOB | 40 | 1 |
| eTraxx_Tik_StartDate | TIMESTAMP | 19 | 1 |
| eTraxx_Tik_StopDate | TIMESTAMP | 19 | 1 |
| eTraxx_Tik_DateStore | INT32 | 11 | 1 |
| Prefers_email_Invoice | BOOLEAN | 5 | 1 |
| RFC | CLOB | 13 | 1 |
| Method_of_Payment | CLOB | 40 | 1 |
| PK_UUID | UUID | 0 | 1 |
| Serialnumber | CLOB | 20 | 1 |
| AE_PrefAppMethod | CLOB | 0 | 1 |
| On_hold | BOOLEAN | 5 | 1 |
| enableAP | BOOLEAN | 5 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |
| Est_Duration | INT32 | 11 | 1 |
| Est_DurationUnlimited | BOOLEAN | 5 | 1 |
| unused_106 | BOOLEAN | 5 | 1 |
| contractTermExpiration | TIMESTAMP | 19 | 1 |
| nextPaymentPeriod | TIMESTAMP | 19 | 1 |
| LogoBMP | BLOB | 0 | 1 |

### CustomerProduct

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| StockProdID | CLOB | 10 | 1 |
| CustomerID | CLOB | 10 | 1 |
| CustProdNo | CLOB | 30 | 1 |
| PK_UUID | UUID | 0 | 1 |

### DASH_Goal

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |
| Bundle_ID | INT32 | 11 | 1 |
| AcctYear_ID | INT32 | 11 | 1 |
| AccYear_Month | INT32 | 11 | 1 |
| Month_Name | CLOB | 10 | 1 |
| MonthEndDate | TIMESTAMP | 19 | 1 |
| Goal | REAL | 7 | 1 |
| Num_Employees | INT32 | 11 | 1 |

### DASH_Goal_Bundle

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| Name | CLOB | 30 | 1 |
| Name_Rsc_FormNo | INT32 | 11 | 1 |
| Name_Rsc_ItemNo | INT32 | 11 | 1 |
| Group_ID | CLOB | 30 | 1 |
| PK_UUID | UUID | 0 | 0 |
| Sort_Order | INT32 | 11 | 1 |
| Has_Annual_Goals | BOOLEAN | 5 | 1 |
| Goal_Fields | None | 0 | 1 |
| Aging | BOOLEAN | 5 | 1 |
| EBITDA | None | 0 | 1 |

### DASH_Graph

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| Name | CLOB | 40 | 1 |
| Name_Rsc_FormNo | INT32 | 11 | 1 |
| Name_Rsc_ItemNo | INT32 | 11 | 1 |
| Help_Text | CLOB | 0 | 1 |
| Group_ID | CLOB | 10 | 1 |
| PK_UUID | UUID | 0 | 1 |
| Sort_Order | INT32 | 11 | 1 |
| Goal_Bundle_ID | INT32 | 11 | 1 |
| Help_Rsc_FormNo | INT32 | 11 | 1 |
| Help_Rsc_ItemNo | INT32 | 11 | 1 |
| Available | BOOLEAN | 5 | 1 |
| Wiki | CLOB | 255 | 1 |
| Use_End_Of_Month | BOOLEAN | 5 | 1 |

### DASH_Graph_Group

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| Name | CLOB | 30 | 1 |
| PK_UUID | UUID | 0 | 1 |
| Name_Rsc_FormNo | INT32 | 11 | 1 |
| Name_Rsc_ItemNo | INT32 | 11 | 1 |
| Sort_Order | INT32 | 11 | 1 |

### DASH_Preference

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| Employee_Number | CLOB | 10 | 1 |
| Permissions | None | 0 | 1 |
| PK_UUID | UUID | 0 | 1 |
| Favorites | None | 0 | 1 |
| Dates | None | 0 | 1 |

### Dialogs

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| Utility_File | BOOLEAN | 5 | 1 |
| PK_UUID | UUID | 0 | 1 |

### DieChart

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| Items_subtable | INT32 | 11 | 1 |
| TD_125_CP | INT16 | 6 | 1 |
| TD_32_DP | INT16 | 6 | 1 |
| TD_25_CP | INT16 | 6 | 1 |
| Module_1 | INT16 | 6 | 1 |
| TD_0625_CP | INT16 | 6 | 1 |
| CP_1666 | INT16 | 6 | 1 |
| PK_UUID | UUID | 0 | 1 |

### DieChart_Item

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| DieChart_ID | CLOB | 10 | 1 |
| Die_Size | REAL | 7 | 1 |
| Steel | CLOB | 15 | 1 |
| iType | CLOB | 20 | 1 |
| Price | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |

### DieHardnessRates

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| Description | CLOB | 15 | 1 |
| PricePerLinealInch | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |

### DupTemp

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ContactID | CLOB | 10 | 1 |
| ContactName | CLOB | 80 | 1 |
| Address1 | CLOB | 255 | 1 |
| Address2 | CLOB | 255 | 1 |
| City | CLOB | 40 | 1 |
| State_Province | CLOB | 40 | 1 |
| Zip | CLOB | 15 | 1 |
| Country | CLOB | 40 | 1 |
| Phone | CLOB | 20 | 1 |
| Fax | CLOB | 20 | 1 |
| fName | CLOB | 80 | 1 |
| lName | CLOB | 80 | 1 |
| email | CLOB | 80 | 1 |
| MarketingSource | CLOB | 40 | 1 |
| SalesRepNo | CLOB | 10 | 1 |
| CustServNo | CLOB | 10 | 1 |
| PK_UUID | UUID | 0 | 1 |
| AE_PrefApproveMethod | CLOB | 0 | 1 |
| On_hold | BOOLEAN | 5 | 1 |

### EP_ElectronicPayments

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| PaymentDate | TIMESTAMP | 19 | 1 |
| Description | CLOB | 80 | 1 |
| BankAccountName | CLOB | 30 | 1 |
| AP_BankAccount_ID | INT32 | 11 | 1 |
| AcctBalanceB4_EP | REAL | 7 | 1 |
| Total_EP_Amount | REAL | 7 | 1 |
| AcctBalanceAfter_EP | REAL | 7 | 1 |
| Total_EP_Discount | REAL | 7 | 1 |
| AP_PostingStatus | CLOB | 10 | 1 |
| GL_PostingStatus | CLOB | 10 | 1 |
| GL_Detail_ID | INT32 | 11 | 1 |
| GL_Detail_ID_DiscDebit | INT32 | 11 | 1 |
| GL_Detail_ID_DiscCredit | INT32 | 11 | 1 |
| EnteredBy | CLOB | 50 | 1 |
| EnteredDate | TIMESTAMP | 19 | 1 |
| EnteredTime | INTERVAL | 10 | 1 |
| ModifiedBy | CLOB | 50 | 1 |
| ModifiedDate | TIMESTAMP | 19 | 1 |
| ModifiedTime | INTERVAL | 10 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### EP_ItemsPaid

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| EP_ElectronicPayment_ID | INT32 | 11 | 1 |
| EP_SupplierTotals_ID | INT32 | 11 | 1 |
| AP_Balance_ID | INT32 | 11 | 1 |
| Payment_Amount | REAL | 7 | 1 |
| DiscountTaken | REAL | 7 | 1 |
| Pay | BOOLEAN | 5 | 1 |
| Force | BOOLEAN | 5 | 1 |
| SupplierNum | INT32 | 11 | 1 |
| SupplierName | CLOB | 80 | 1 |
| InvoiceNumber | CLOB | 20 | 1 |
| InvoiceDate | TIMESTAMP | 19 | 1 |
| SupplierNameNumSortKey | CLOB | 60 | 1 |
| AP_Transaction_ID | INT32 | 11 | 1 |
| NewPrepayment | BOOLEAN | 5 | 1 |
| PaymentDate | TIMESTAMP | 19 | 1 |
| CurrencyIndicator | CLOB | 10 | 1 |
| InvoiceCurrency_ID | INT32 | 11 | 1 |
| FCT_PaymentAmount | REAL | 7 | 1 |
| FCT_CurrencyAdjust | REAL | 7 | 1 |
| FCT_DiscountTaken | REAL | 7 | 1 |
| Pay_Currency_ExchRate | REAL | 7 | 1 |
| GL_Detail_ID_CurrAdj | INT32 | 11 | 1 |
| GL_Detail_ID_CurrAdj_AP | INT32 | 11 | 1 |
| BalanceDueBefore | REAL | 7 | 1 |
| FCT_BalanceDueBefore | REAL | 7 | 1 |
| BalanceDueAfter | REAL | 7 | 1 |
| FCT_BalanceDueAfter | REAL | 7 | 1 |
| Supplier_AccountNumber | CLOB | 255 | 1 |
| Bank_ID | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |

### EP_SupplierTotals

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| EP_ElectronicPayment_ID | INT32 | 11 | 1 |
| Payment_Ref_ID | CLOB | 80 | 1 |
| SupplierName | CLOB | 80 | 1 |
| TotalPaymentAmount | REAL | 7 | 1 |
| GL_Detail_ID | INT32 | 11 | 1 |
| PaymentDate | TIMESTAMP | 19 | 1 |
| FCT_TotalPaymentAmount | REAL | 7 | 1 |
| TotalDiscount | REAL | 7 | 1 |
| FCT_TotalDiscount | REAL | 7 | 1 |
| FCT_TotalCurrAdj | REAL | 7 | 1 |
| SupplierNum | INT32 | 11 | 1 |
| SupplierBankInfo | CLOB | 0 | 1 |
| Bank_ID | INT32 | 11 | 1 |
| Suplier_Accountnumber | CLOB | 255 | 1 |
| PK_UUID | UUID | 0 | 1 |

### ETraxx_Constants

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| Is_Authorization_Required | BOOLEAN | 5 | 1 |
| Is_Self_Authorization_Allowed | BOOLEAN | 5 | 1 |
| Default_Prospect_ID | CLOB | 10 | 1 |
| Default_Prospect_Name | CLOB | 80 | 1 |
| FTP_FileSize_Limit | INT32 | 11 | 1 |
| Session_TimeOut | INT32 | 11 | 1 |
| FTP_FolderLocation | CLOB | 0 | 1 |
| Default_Prospect_WebPass | CLOB | 20 | 1 |
| EMail_From | CLOB | 80 | 1 |
| EMail_UserName | CLOB | 80 | 1 |
| EMail_Password | CLOB | 80 | 1 |
| LaminateButtonPop | BOOLEAN | 5 | 1 |
| StockButtonPop | BOOLEAN | 5 | 1 |
| ipAddress | CLOB | 80 | 1 |
| Web_Email_Template | CLOB | 0 | 1 |
| Record_Listing_Limit | INT32 | 11 | 1 |
| Require_Account | BOOLEAN | 5 | 1 |
| DefaultHTML_Root | CLOB | 0 | 1 |
| PK_UUID | UUID | 0 | 1 |

### ETraxx_Email

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| eTraxx_Constants_ID | CLOB | 10 | 1 |
| Email_Identifier | CLOB | 20 | 1 |
| Email_Address | CLOB | 80 | 1 |
| Prospect_Entered | BOOLEAN | 5 | 1 |
| Estimate_Requested | BOOLEAN | 5 | 1 |
| Order_Request | BOOLEAN | 5 | 1 |
| Artwork_Uploaded | BOOLEAN | 5 | 1 |
| Ticket_Reorder | BOOLEAN | 5 | 1 |
| Error_for_WebMasters | BOOLEAN | 5 | 1 |
| Entered_By | CLOB | 80 | 1 |
| Entered_Date | TIMESTAMP | 19 | 1 |
| Entered_Time | INTERVAL | 10 | 1 |
| Modified_By | CLOB | 80 | 1 |
| Modified_Date | TIMESTAMP | 19 | 1 |
| Modified_Time | INTERVAL | 10 | 1 |
| Product_Approval | BOOLEAN | 5 | 1 |
| Forecast_Update | BOOLEAN | 5 | 1 |
| Shopping_Cart | BOOLEAN | 5 | 1 |
| Digital_Est_Requested | BOOLEAN | 5 | 1 |
| Cust_Serv_Name | CLOB | 35 | 1 |
| Cust_Serv_No | CLOB | 10 | 1 |
| Sales_Rep_Name | CLOB | 35 | 1 |
| Sales_Rep_No | CLOB | 10 | 1 |
| PK_UUID | UUID | 0 | 1 |

### ETraxx_Estimate

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| eTraxx_Constants_ID | CLOB | 10 | 1 |
| Default_Press_ID | CLOB | 10 | 1 |
| Default_Equip_ID | CLOB | 10 | 1 |
| Main_Web_Width | REAL | 7 | 1 |
| Default_Product_Group | CLOB | 40 | 1 |
| Delivery_Upcharge1_Title | CLOB | 40 | 1 |
| Delivery_Upcharge1_Fee | REAL | 7 | 1 |
| Delivery_Upcharge2_Title | CLOB | 40 | 1 |
| Delivery_Upcharge2_Fee | REAL | 7 | 1 |
| Laminate_Web_Width | REAL | 7 | 1 |
| Default_UpCharge_Default | CLOB | 40 | 1 |
| Max_Allowed_Amount | REAL | 7 | 1 |
| Default_Labels_Group | CLOB | 40 | 1 |
| Default_FloodInk_Type | CLOB | 30 | 1 |
| Default_FloodInk_Qty | INT32 | 11 | 1 |
| Default_FloodInk_Coverage | INT16 | 6 | 1 |
| Is_Maximize_Labels_On | BOOLEAN | 5 | 1 |
| LaminateButtonPop | BOOLEAN | 5 | 1 |
| StockButtonPop | BOOLEAN | 5 | 1 |
| LaserDieCutter | BOOLEAN | 5 | 1 |
| Default_PrintInkType | CLOB | 255 | 1 |
| Default_PrintInk_1_NoColors | INT16 | 6 | 1 |
| Default_PrintInk_1_Coverage | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |

### ETraxx_Log

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 20 | 1 |
| Users | CLOB | 80 | 1 |
| Date_Created | TIMESTAMP | 19 | 1 |
| Time_Created | INTERVAL | 10 | 1 |
| Location | CLOB | 80 | 1 |
| TOC | CLOB | 80 | 1 |
| SessionID | CLOB | 80 | 1 |
| IP_Address | CLOB | 20 | 1 |
| Notes | CLOB | 0 | 1 |
| Parent | CLOB | 80 | 1 |
| Type_TOC | INT16 | 6 | 1 |
| PK_UUID | UUID | 0 | 1 |

### ETraxx_Prospect

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| eTraxx_Constants_ID | CLOB | 10 | 1 |
| Sales_Rep_No | CLOB | 10 | 1 |
| Sales_Rep_Name | CLOB | 35 | 1 |
| Cust_Serv_No | CLOB | 10 | 1 |
| Cust_Serv_Name | CLOB | 35 | 1 |
| Market_Source | CLOB | 20 | 1 |
| ProfitAdjLabel | CLOB | 20 | 1 |
| Terms | CLOB | 45 | 1 |
| CreditStatus | BOOLEAN | 5 | 1 |
| Credit_Limit | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |

### ETraxx_Website_Text

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| eTraxx_Constants_ID | CLOB | 10 | 1 |
| ID_Name | CLOB | 40 | 1 |
| HTML_Text | CLOB | 0 | 1 |
| PK_UUID | UUID | 0 | 1 |

### EXT_FileStorage

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 0 | 1 |
| EXT_FileLink | BLOB | 0 | 1 |
| FileName | CLOB | 0 | 1 |
| FileType | CLOB | 0 | 1 |
| FileSize | REAL | 7 | 1 |
| DateImported | TIMESTAMP | 19 | 1 |
| WhoCreatedID | CLOB | 0 | 1 |
| TimeImported | INTERVAL | 10 | 1 |
| ExtNotes | CLOB | 0 | 1 |
| PK_UUID | UUID | 0 | 1 |
| FilePath | CLOB | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### EXT_Reference

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 0 | 1 |
| TableNum | INT32 | 11 | 1 |
| FieldID | CLOB | 0 | 1 |
| EXT_FileID | CLOB | 0 | 1 |
| GroupID | CLOB | 0 | 1 |
| CustNo | CLOB | 0 | 1 |
| CustName | CLOB | 0 | 1 |
| TableName | CLOB | 0 | 1 |
| not_used | INT16 | 6 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### EmailObjects

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| PK_UUID | UUID | 0 | 0 |
| associateNumber | CLOB | 255 | 1 |
| emailSigniture | None | 0 | 1 |

### EmployeeStatus

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| AssocNum | CLOB | 10 | 1 |
| PunchedInOut | CLOB | 20 | 1 |
| PunchInDate | TIMESTAMP | 19 | 1 |
| PunchInTime | INTERVAL | 10 | 1 |
| PunchOutDate | TIMESTAMP | 19 | 1 |
| PunchOutTime | INTERVAL | 10 | 1 |
| OpenTCRecID | CLOB | 10 | 1 |
| CurrentOperatio | CLOB | 20 | 1 |
| NextOperation | CLOB | 20 | 1 |
| TicketNum | CLOB | 12 | 1 |
| Current_Group | CLOB | 20 | 1 |
| Department | CLOB | 20 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### Employee_Preference

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| Employee_Number | CLOB | 10 | 1 |
| FormPage_Key | CLOB | 120 | 1 |
| SS_ALP_ColumnWidths | BLOB | 0 | 1 |
| PK_UUID | UUID | 0 | 1 |
| prefData | None | 0 | 1 |
| FontSize | INT16 | 6 | 1 |

### Empty_Multiuser

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| u1 | CLOB | 0 | 1 |
| u2 | CLOB | 0 | 1 |
| u3 | CLOB | 0 | 1 |
| u4 | CLOB | 0 | 1 |
| PK_UUID | UUID | 0 | 1 |

### Encoder_License

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| IP_Address | CLOB | 80 | 1 |
| WorkStationName | CLOB | 80 | 1 |
| Issued_UTC | CLOB | 80 | 1 |
| Released_UTC | CLOB | 80 | 1 |
| PK_UUID | UUID | 0 | 1 |

### Equip_InkTypesAndRates

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| EquipmentNumber | CLOB | 10 | 1 |
| InkType | CLOB | 20 | 1 |
| DollarsPerMSI | REAL | 7 | 1 |
| MinimumInkCharge | REAL | 7 | 1 |
| DefaultPrintInk | BOOLEAN | 5 | 1 |
| DefaultFloodInk | BOOLEAN | 5 | 1 |
| PK_UUID | UUID | 0 | 1 |
| ID | INT32 | 11 | 1 |
| Equipment_ID | INT32 | 11 | 1 |
| Ink_Weight | REAL | 7 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### Equip_RatesByNumberOfColors

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| EquipmentNumber | CLOB | 10 | 1 |
| NumberOfColors | INT32 | 11 | 1 |
| EstimateRate | REAL | 7 | 1 |
| WIP_Rate | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 255 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### Equip_SemiRotary

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| PK_UUID | UUID | 0 | 1 |
| Equip_ID | INT32 | 11 | 1 |
| Equip_Number | CLOB | 10 | 1 |
| Speed_Chart | None | 0 | 1 |
| Chart_Source | CLOB | 80 | 1 |

### Equip_UserDefined

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| Press_Number | CLOB | 10 | 1 |
| Description | CLOB | 20 | 1 |
| MakeReadyHours | REAL | 7 | 1 |
| WashUpHours | REAL | 7 | 1 |
| SpeedChange | REAL | 7 | 1 |
| SpoilageChange | REAL | 7 | 1 |
| PressProfiler | BOOLEAN | 5 | 1 |
| Print_On_Reports | BOOLEAN | 5 | 1 |
| Order_in_List | INT32 | 11 | 1 |
| Add_Web_Width | REAL | 7 | 1 |
| Stock_SetUp_Length | REAL | 7 | 1 |
| Option_Multiplier | REAL | 7 | 1 |
| Add_Hourly_Est_Rate | REAL | 7 | 1 |
| Add_Hourly_WIP_Rate | REAL | 7 | 1 |
| Add_Run_Length | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 255 | 1 |

### Equipment

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| Number | CLOB | 10 | 1 |
| PType | CLOB | 25 | 1 |
| MaxStockWidth | REAL | 7 | 1 |
| MinStockWidth | REAL | 7 | 1 |
| MaxColors | INT16 | 6 | 1 |
| MaxTools | INT16 | 6 | 1 |
| MaxPrintRepeat | REAL | 7 | 1 |
| MinPrintRepeat | REAL | 7 | 1 |
| MaxDieRepeat | REAL | 7 | 1 |
| MinDieRepeat | REAL | 7 | 1 |
| MaxPrintWidth | REAL | 7 | 1 |
| UVCoat | REAL | 7 | 1 |
| ConsecutiveNo | REAL | 7 | 1 |
| Turnbar | REAL | 7 | 1 |
| Sheeter | REAL | 7 | 1 |
| WIP_Rate | REAL | 7 | 1 |
| EstimateRate | REAL | 7 | 1 |
| PrintInkCost | REAL | 7 | 1 |
| FloodInkCost | REAL | 7 | 1 |
| Description | CLOB | 35 | 1 |
| Notes | CLOB | 0 | 1 |
| MRFirstDie | REAL | 7 | 1 |
| MRAdditonalDie | REAL | 7 | 1 |
| MRFirstColor | REAL | 7 | 1 |
| MRAdditionalCol | REAL | 7 | 1 |
| MRFlood | REAL | 7 | 1 |
| SetupFeet | REAL | 7 | 1 |
| MRStock | REAL | 7 | 1 |
| WUFirstColor | REAL | 7 | 1 |
| WUFloods | REAL | 7 | 1 |
| WUDie | REAL | 7 | 1 |
| PressSpeed1 | INT16 | 6 | 1 |
| PressSpeed2 | INT16 | 6 | 1 |
| PressSpeed3 | INT16 | 6 | 1 |
| MinPrintInk | REAL | 7 | 1 |
| MinFloodInk | REAL | 7 | 1 |
| PinfeedPunch | REAL | 7 | 1 |
| StockSpoilL1 | INT32 | 11 | 1 |
| StockSpoilH1 | INT32 | 11 | 1 |
| StockSpoilPerc1 | REAL | 7 | 1 |
| StockSpoilL2 | INT32 | 11 | 1 |
| StockSpoilH2 | INT32 | 11 | 1 |
| StockSpoilPerc2 | REAL | 7 | 1 |
| StockSpoilL3 | INT32 | 11 | 1 |
| StockSpoilH3 | INT32 | 11 | 1 |
| StockSpoilPerc3 | REAL | 7 | 1 |
| StockSpoilL4 | INT32 | 11 | 1 |
| StockSpoilH4 | INT32 | 11 | 1 |
| StockSpoilPerc4 | REAL | 7 | 1 |
| StockSpoilL5 | INT32 | 11 | 1 |
| StockSpoilH5 | INT32 | 11 | 1 |
| StockSpoilPerc5 | REAL | 7 | 1 |
| PressSpeed4 | INT16 | 6 | 1 |
| PressSpeed5 | INT16 | 6 | 1 |
| Inactive | BOOLEAN | 5 | 1 |
| HSPlateCost | REAL | 7 | 1 |
| HSStockSpoil | REAL | 7 | 1 |
| HSToolCost | REAL | 7 | 1 |
| ConsecutLimit | INT16 | 6 | 1 |
| CylinderSize | CLOB | 6 | 1 |
| CommercialJC | REAL | 7 | 1 |
| DistributorJC | REAL | 7 | 1 |
| PlateChangeCharge | REAL | 7 | 1 |
| ColorChangeCharge | REAL | 7 | 1 |
| ModifiedDate | TIMESTAMP | 19 | 1 |
| Pitch | CLOB | 8 | 1 |
| PressureAngle | REAL | 7 | 1 |
| StockSpoilL6 | INT32 | 11 | 1 |
| StockSpoilL7 | INT32 | 11 | 1 |
| StockSpoilL8 | INT32 | 11 | 1 |
| StockSpoilL9 | INT32 | 11 | 1 |
| StockSpoilL10 | INT32 | 11 | 1 |
| StockSpoilL11 | INT32 | 11 | 1 |
| StockSpoilL12 | INT32 | 11 | 1 |
| StockSpoilL13 | INT32 | 11 | 1 |
| StockSpoilL14 | INT32 | 11 | 1 |
| StockSpoilL15 | INT32 | 11 | 1 |
| StockSpoilL16 | INT32 | 11 | 1 |
| StockSpoilL17 | INT32 | 11 | 1 |
| StockSpoilL18 | INT32 | 11 | 1 |
| StockSpoilL19 | INT32 | 11 | 1 |
| StockSpoilL20 | INT32 | 11 | 1 |
| StockSpoilH6 | INT32 | 11 | 1 |
| StockSpoilH7 | INT32 | 11 | 1 |
| StockSpoilH8 | INT32 | 11 | 1 |
| StockSpoilH9 | INT32 | 11 | 1 |
| StockSpoilH10 | INT32 | 11 | 1 |
| StockSpoilH11 | INT32 | 11 | 1 |
| StockSpoilH12 | INT32 | 11 | 1 |
| StockSpoilH13 | INT32 | 11 | 1 |
| StockSpoilH14 | INT32 | 11 | 1 |
| StockSpoilH15 | INT32 | 11 | 1 |
| StockSpoilH16 | INT32 | 11 | 1 |
| StockSpoilH17 | INT32 | 11 | 1 |
| StockSpoilH18 | INT32 | 11 | 1 |
| StockSpoilH19 | INT32 | 11 | 1 |
| StockSpoilH20 | INT32 | 11 | 1 |
| StockSpoilPerc6 | REAL | 7 | 1 |
| StockSpoilPerc7 | REAL | 7 | 1 |
| StockSpoilPerc8 | REAL | 7 | 1 |
| StockSpoilPerc9 | REAL | 7 | 1 |
| StockSpoilPer10 | REAL | 7 | 1 |
| StockSpoilPer11 | REAL | 7 | 1 |
| StockSpoilPer12 | REAL | 7 | 1 |
| StockSpoilPer13 | REAL | 7 | 1 |
| StockSpoilPer14 | REAL | 7 | 1 |
| StockSpoilPer15 | REAL | 7 | 1 |
| StockSpoilPer16 | REAL | 7 | 1 |
| StockSpoilPer17 | REAL | 7 | 1 |
| StockSpoilPer18 | REAL | 7 | 1 |
| StockSpoilPer19 | REAL | 7 | 1 |
| StockSpoilPer20 | REAL | 7 | 1 |
| PressSpeed6 | INT16 | 6 | 1 |
| PressSpeed7 | INT16 | 6 | 1 |
| PressSpeed8 | INT16 | 6 | 1 |
| PressSpeed9 | INT16 | 6 | 1 |
| PressSpeed10 | INT16 | 6 | 1 |
| PressSpeed11 | INT16 | 6 | 1 |
| PressSpeed12 | INT16 | 6 | 1 |
| PressSpeed13 | INT16 | 6 | 1 |
| PressSpeed14 | INT16 | 6 | 1 |
| PressSpeed15 | INT16 | 6 | 1 |
| PressSpeed16 | INT16 | 6 | 1 |
| PressSpeed17 | INT16 | 6 | 1 |
| PressSpeed18 | INT16 | 6 | 1 |
| PressSpeed19 | INT16 | 6 | 1 |
| PressSpeed20 | INT16 | 6 | 1 |
| ModifiedTime | INTERVAL | 10 | 1 |
| PlateChgHr | REAL | 7 | 1 |
| ColorChgHr | REAL | 7 | 1 |
| MachineCount | REAL | 7 | 1 |
| UserDef_MR_1Lbl | CLOB | 20 | 1 |
| UserDef_MR_1Hrs | REAL | 7 | 1 |
| UserDef_MR_2Lbl | CLOB | 20 | 1 |
| UserDef_MR_2Hrs | REAL | 7 | 1 |
| AvailSchedHours | REAL | 7 | 1 |
| OmitFromSched | CLOB | 20 | 1 |
| DefaultRewinder | BOOLEAN | 5 | 1 |
| MinimumPressSpeed | INT32 | 11 | 1 |
| MaximumPressSpeed | INT32 | 11 | 1 |
| MinimumStockSpoilage | REAL | 7 | 1 |
| MaximumStockSpoilage | REAL | 7 | 1 |
| ConsecutiveNum_SpeedChange | REAL | 7 | 1 |
| ConsecutiveNum_SpoilageChange | REAL | 7 | 1 |
| Turnbar_SpeedChange | REAL | 7 | 1 |
| Turnbar_SpoilageChange | REAL | 7 | 1 |
| Sheeter_SpeedChange | REAL | 7 | 1 |
| Sheeter_SpoilageChange | REAL | 7 | 1 |
| Pinfeed_SpeedChange | REAL | 7 | 1 |
| Pinfeed_SpoilageChange | REAL | 7 | 1 |
| UserDef_MR_1_SpeedChange | REAL | 7 | 1 |
| UserDef_MR_1_SpoilageChange | REAL | 7 | 1 |
| UserDef_MR_2_SpeedChange | REAL | 7 | 1 |
| UserDef_MR_2_SpoilageChange | REAL | 7 | 1 |
| MRFirstDie_SpeedChange | REAL | 7 | 1 |
| MRFirstDie_SpoilageChange | REAL | 7 | 1 |
| MRAdd_Dies_SpeedChange | REAL | 7 | 1 |
| MRAdd_Dies_SpoilageChange | REAL | 7 | 1 |
| MRFirstColor_SpeedChange | REAL | 7 | 1 |
| MRFirstColor_SpoilageChange | REAL | 7 | 1 |
| MRAdd_Colors_SpeedChange | REAL | 7 | 1 |
| MRAdd_Colors_SpoilageChange | REAL | 7 | 1 |
| MRFlood_SpeedChange | REAL | 7 | 1 |
| MRFlood_SpoilageChange | REAL | 7 | 1 |
| MRStock_SpeedChange | REAL | 7 | 1 |
| MRStock_SpoilageChange | REAL | 7 | 1 |
| PlateChange_SpeedChange | REAL | 7 | 1 |
| PlateChange_SetUpFootChange | INT32 | 11 | 1 |
| ColorChange_SpeedChange | REAL | 7 | 1 |
| ColorChange_SetUpFootChange | INT32 | 11 | 1 |
| MR_Max1 | INT32 | 11 | 1 |
| MR_Max2 | INT32 | 11 | 1 |
| MR_Max3 | INT32 | 11 | 1 |
| MR_Max4 | INT32 | 11 | 1 |
| MR_Max5 | INT32 | 11 | 1 |
| MR_Max6 | INT32 | 11 | 1 |
| MR_Desc1 | CLOB | 30 | 1 |
| MR_Desc2 | CLOB | 30 | 1 |
| MR_Desc3 | CLOB | 30 | 1 |
| MR_Desc4 | CLOB | 30 | 1 |
| MR_Desc5 | CLOB | 30 | 1 |
| MR_Desc6 | CLOB | 30 | 1 |
| MR_Hours1 | REAL | 7 | 1 |
| MR_Hours2 | REAL | 7 | 1 |
| MR_Hours3 | REAL | 7 | 1 |
| MR_Hours4 | REAL | 7 | 1 |
| MR_Hours5 | REAL | 7 | 1 |
| MR_Hours6 | REAL | 7 | 1 |
| PhotoPolymerThickness | REAL | 7 | 1 |
| PolyesterBackingThickness | REAL | 7 | 1 |
| Impression_Charge | REAL | 7 | 1 |
| ModifiedBy | CLOB | 0 | 1 |
| EnteredBy | CLOB | 50 | 1 |
| EnteredDate | TIMESTAMP | 19 | 1 |
| EnteredTime | INTERVAL | 10 | 1 |
| ImpressionCharge_1_color | REAL | 7 | 1 |
| ImpressionCharge_2_color | REAL | 7 | 1 |
| HP_Indigo_Model | CLOB | 30 | 1 |
| Has_TurretRewinder | BOOLEAN | 5 | 1 |
| InternetQuery | BOOLEAN | 5 | 1 |
| Rewind_MR_per_FInished_Roll | REAL | 7 | 1 |
| Rewind_Add_Roll_SpeedChange | REAL | 7 | 1 |
| Is_Est_Max_up_on | BOOLEAN | 5 | 1 |
| Lineal_Length_Rate | REAL | 7 | 1 |
| Is_ShrinkSleeve_Capable | BOOLEAN | 5 | 1 |
| Is_DigitalCoating_Required | BOOLEAN | 5 | 1 |
| Is_Print_Roll_Alert_Omitted | BOOLEAN | 5 | 1 |
| BackStage_SmartMarkSet_Default | CLOB | 40 | 1 |
| Est_Are_Tools_for_Equip | BOOLEAN | 5 | 1 |
| Is_Allowed_Rotary_Die | BOOLEAN | 5 | 1 |
| Is_Allowed_SemiRotary_Die | BOOLEAN | 5 | 1 |
| Is_Allowed_Flatbed_Die | BOOLEAN | 5 | 1 |
| Omit_MakeReady_Cycle | BOOLEAN | 5 | 1 |
| Omit_WashUp_Cycle | BOOLEAN | 5 | 1 |
| HP_Indigo_EPM_Markup | REAL | 7 | 1 |
| ID | INT32 | 11 | 1 |
| Rotometrics_NeedsID | BOOLEAN | 5 | 1 |
| aLC_Is_aLaCarte_Pricing | BOOLEAN | 5 | 1 |
| aLC_White_Charge | REAL | 7 | 1 |
| aLC_Color_Charge | REAL | 7 | 1 |
| HP_Indigo_PriceMethod | INT32 | 11 | 1 |
| HP_Indigo_PriceChart_Limit_1 | INT32 | 11 | 1 |
| HP_Indigo_PriceChart_Limit_2 | INT32 | 11 | 1 |
| HP_Indigo_PriceChart_Limit_3 | INT32 | 11 | 1 |
| HP_Indigo_PriceChart_Limit_4 | INT32 | 11 | 1 |
| HP_Indigo_PriceChart_Limit_5 | INT32 | 11 | 1 |
| HP_Indigo_PriceChart_Limit_6 | INT32 | 11 | 1 |
| HP_Indigo_PriceChart_Limit_7 | INT32 | 11 | 1 |
| HP_Indigo_PriceChart_Limit_8 | INT32 | 11 | 1 |
| HP_Indigo_PriceChart_InkCost_1 | REAL | 7 | 1 |
| HP_Indigo_PriceChart_InkCost_2 | REAL | 7 | 1 |
| HP_Indigo_PriceChart_InkCost_3 | REAL | 7 | 1 |
| HP_Indigo_PriceChart_InkCost_4 | REAL | 7 | 1 |
| HP_Indigo_PriceChart_InkCost_5 | REAL | 7 | 1 |
| HP_Indigo_PriceChart_InkCost_6 | REAL | 7 | 1 |
| HP_Indigo_PriceChart_InkCost_7 | REAL | 7 | 1 |
| HP_Indigo_PriceChart_InkCost_8 | REAL | 7 | 1 |
| JMF_Device_ID | CLOB | 255 | 1 |
| Pitch_Local | CLOB | 0 | 1 |
| PType_Local | CLOB | 0 | 1 |
| Trim_width | REAL | 7 | 1 |
| VS_Events_Auto_Generate | BOOLEAN | 5 | 1 |
| VS_Start | INTERVAL | 10 | 1 |
| VS_End | INTERVAL | 10 | 1 |
| VS_Mon | BOOLEAN | 5 | 1 |
| VS_Tue | BOOLEAN | 5 | 1 |
| VS_Wed | BOOLEAN | 5 | 1 |
| VS_Thu | BOOLEAN | 5 | 1 |
| VS_Fri | BOOLEAN | 5 | 1 |
| VS_Sat | BOOLEAN | 5 | 1 |
| VS_Sun | BOOLEAN | 5 | 1 |
| CMYOVG_ClickCharge | REAL | 7 | 1 |
| CMYOVG_InkCost | REAL | 7 | 1 |
| CMYOVG_InkCoverage | REAL | 7 | 1 |
| White_ClickCharge | REAL | 7 | 1 |
| White_InkCost | REAL | 7 | 1 |
| White_InkCoverage | REAL | 7 | 1 |
| Black_ClickCharge | REAL | 7 | 1 |
| Black_InkCost | REAL | 7 | 1 |
| Black_InkCoverage | REAL | 7 | 1 |
| Silver_ClickCharge | REAL | 7 | 1 |
| Silver_InkCost | REAL | 7 | 1 |
| Silver_InkCoverage | REAL | 7 | 1 |
| Other_ClickCharge | REAL | 7 | 1 |
| Other_InkCost | REAL | 7 | 1 |
| Other_InkCoverage | REAL | 7 | 1 |
| MaterialPrimer_AreaRate | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |
| Toner_Inventory_ID | CLOB | 10 | 1 |
| SC_Downtimes | INT16 | 6 | 1 |
| CMYOVG_WeightPerArea | REAL | 7 | 1 |
| White_WeightPerArea | REAL | 7 | 1 |
| Black_WeightPerArea | REAL | 7 | 1 |
| Silver_WeightPerArea | REAL | 7 | 1 |
| Other_WeightPerArea | REAL | 7 | 1 |
| SemiRotary_CylinderSize | REAL | 7 | 1 |
| PressMfg | CLOB | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |
| Tag | CLOB | 3 | 1 |

### Est_AddlStock

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| EstimateNumber | CLOB | 10 | 1 |
| StockNum | CLOB | 10 | 1 |
| Width | REAL | 7 | 1 |
| PricePerMSI | REAL | 7 | 1 |
| Caliper | REAL | 7 | 1 |
| Description | CLOB | 40 | 1 |
| StockPrice_1 | REAL | 7 | 1 |
| StockPrice_2 | REAL | 7 | 1 |
| StockPrice_3 | REAL | 7 | 1 |
| StockPrice_4 | REAL | 7 | 1 |
| StockPrice_5 | REAL | 7 | 1 |
| StockPrice_6 | REAL | 7 | 1 |
| PricePerMSI_Override | BOOLEAN | 5 | 1 |
| PK_UUID | UUID | 0 | 1 |
| RoutingNo | INT16 | 6 | 1 |

### Est_PostPress

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| Estimate_ID | CLOB | 10 | 1 |
| Equip_ID | CLOB | 10 | 1 |
| Equip_Desc | CLOB | 80 | 1 |
| Equip_HourRate | REAL | 7 | 1 |
| Equip_MinCost | REAL | 7 | 1 |
| Operation_Desc | CLOB | 40 | 1 |
| PiecesOperation | INT32 | 11 | 1 |
| Operations_Hour | INT32 | 11 | 1 |
| Material_Desc | CLOB | 40 | 1 |
| Material_Rate | REAL | 7 | 1 |
| Material_Unit | CLOB | 15 | 1 |
| Weight_Piece | REAL | 7 | 1 |
| Option_Desc1 | CLOB | 30 | 1 |
| Option_Desc2 | CLOB | 30 | 1 |
| Option_Desc3 | CLOB | 30 | 1 |
| Option_Desc4 | CLOB | 30 | 1 |
| Option_Desc5 | CLOB | 30 | 1 |
| Option_Desc6 | CLOB | 30 | 1 |
| Option_Hours1 | REAL | 7 | 1 |
| Option_Hours2 | REAL | 7 | 1 |
| Option_Hours3 | REAL | 7 | 1 |
| Option_Hours4 | REAL | 7 | 1 |
| Option_Hours5 | REAL | 7 | 1 |
| Option_Hours6 | REAL | 7 | 1 |
| Option_Qty1 | INT32 | 11 | 1 |
| Option_Qty2 | INT32 | 11 | 1 |
| Option_Qty3 | INT32 | 11 | 1 |
| Option_Qty4 | INT32 | 11 | 1 |
| Option_Qty5 | INT32 | 11 | 1 |
| Option_Qty6 | INT32 | 11 | 1 |
| Option_Max1 | INT32 | 11 | 1 |
| Option_Max2 | INT32 | 11 | 1 |
| Option_Max3 | INT32 | 11 | 1 |
| Option_Max4 | INT32 | 11 | 1 |
| Option_Max5 | INT32 | 11 | 1 |
| Option_Max6 | INT32 | 11 | 1 |
| Option_TotalHrs | REAL | 7 | 1 |
| Operation_Hrs1 | REAL | 7 | 1 |
| Operation_Hrs2 | REAL | 7 | 1 |
| Operation_Hrs3 | REAL | 7 | 1 |
| Operation_Hrs4 | REAL | 7 | 1 |
| Operation_Hrs5 | REAL | 7 | 1 |
| Operation_Hrs6 | REAL | 7 | 1 |
| Total_Hrs1 | REAL | 7 | 1 |
| Total_Hrs2 | REAL | 7 | 1 |
| Total_Hrs3 | REAL | 7 | 1 |
| Total_Hrs4 | REAL | 7 | 1 |
| Total_Hrs5 | REAL | 7 | 1 |
| Total_Hrs6 | REAL | 7 | 1 |
| Labor_Cost1 | REAL | 7 | 1 |
| Labor_Cost2 | REAL | 7 | 1 |
| Labor_Cost3 | REAL | 7 | 1 |
| Labor_Cost4 | REAL | 7 | 1 |
| Labor_Cost5 | REAL | 7 | 1 |
| Labor_Cost6 | REAL | 7 | 1 |
| Material_Cost1 | REAL | 7 | 1 |
| Material_Cost2 | REAL | 7 | 1 |
| Material_Cost3 | REAL | 7 | 1 |
| Material_Cost4 | REAL | 7 | 1 |
| Material_Cost5 | REAL | 7 | 1 |
| Material_Cost6 | REAL | 7 | 1 |
| CopyTimeStamp | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |

### Est_PriceTuner

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| Estimate_ID | CLOB | 10 | 1 |
| PricePerM_AS_1 | REAL | 7 | 1 |
| PricePerM_AS_2 | REAL | 7 | 1 |
| PricePerM_AS_3 | REAL | 7 | 1 |
| PricePerM_AS_4 | REAL | 7 | 1 |
| PricePerM_AS_5 | REAL | 7 | 1 |
| PricePerM_AS_6 | REAL | 7 | 1 |
| PricePerM_TS_1 | REAL | 7 | 1 |
| PricePerM_TS_2 | REAL | 7 | 1 |
| PricePerM_TS_3 | REAL | 7 | 1 |
| PricePerM_TS_4 | REAL | 7 | 1 |
| PricePerM_TS_5 | REAL | 7 | 1 |
| PricePerM_TS_6 | REAL | 7 | 1 |
| PricePerM_EC_1 | REAL | 7 | 1 |
| PricePerM_EC_2 | REAL | 7 | 1 |
| PricePerM_EC_3 | REAL | 7 | 1 |
| PricePerM_EC_4 | REAL | 7 | 1 |
| PricePerM_EC_5 | REAL | 7 | 1 |
| PricePerM_EC_6 | REAL | 7 | 1 |
| ValueAdded_1 | REAL | 7 | 1 |
| ValueAdded_2 | REAL | 7 | 1 |
| ValueAdded_3 | REAL | 7 | 1 |
| ValueAdded_4 | REAL | 7 | 1 |
| ValueAdded_5 | REAL | 7 | 1 |
| ValueAdded_6 | REAL | 7 | 1 |
| Materials_EC_1 | REAL | 7 | 1 |
| Materials_EC_2 | REAL | 7 | 1 |
| Materials_EC_3 | REAL | 7 | 1 |
| Materials_EC_4 | REAL | 7 | 1 |
| Materials_EC_5 | REAL | 7 | 1 |
| Materials_EC_6 | REAL | 7 | 1 |
| Materials_TS_1 | REAL | 7 | 1 |
| Materials_TS_2 | REAL | 7 | 1 |
| Materials_TS_3 | REAL | 7 | 1 |
| Materials_TS_4 | REAL | 7 | 1 |
| Materials_TS_5 | REAL | 7 | 1 |
| Materials_TS_6 | REAL | 7 | 1 |
| Materials_AS_1 | REAL | 7 | 1 |
| Materials_AS_2 | REAL | 7 | 1 |
| Materials_AS_3 | REAL | 7 | 1 |
| Materials_AS_4 | REAL | 7 | 1 |
| Materials_AS_5 | REAL | 7 | 1 |
| Materials_AS_6 | REAL | 7 | 1 |
| Labor_EC_1 | REAL | 7 | 1 |
| Labor_EC_2 | REAL | 7 | 1 |
| Labor_EC_3 | REAL | 7 | 1 |
| Labor_EC_4 | REAL | 7 | 1 |
| Labor_EC_5 | REAL | 7 | 1 |
| Labor_EC_6 | REAL | 7 | 1 |
| Labor_TS_1 | REAL | 7 | 1 |
| Labor_TS_2 | REAL | 7 | 1 |
| Labor_TS_3 | REAL | 7 | 1 |
| Labor_TS_4 | REAL | 7 | 1 |
| Labor_TS_5 | REAL | 7 | 1 |
| Labor_TS_6 | REAL | 7 | 1 |
| Labor_AS_1 | REAL | 7 | 1 |
| Labor_AS_2 | REAL | 7 | 1 |
| Labor_AS_3 | REAL | 7 | 1 |
| Labor_AS_4 | REAL | 7 | 1 |
| Labor_AS_5 | REAL | 7 | 1 |
| Labor_AS_6 | REAL | 7 | 1 |
| Other_1 | REAL | 7 | 1 |
| Other_2 | REAL | 7 | 1 |
| Other_3 | REAL | 7 | 1 |
| Other_4 | REAL | 7 | 1 |
| Other_5 | REAL | 7 | 1 |
| Other_6 | REAL | 7 | 1 |
| Commission_1 | REAL | 7 | 1 |
| Commission_2 | REAL | 7 | 1 |
| Commission_3 | REAL | 7 | 1 |
| Commission_4 | REAL | 7 | 1 |
| Commission_5 | REAL | 7 | 1 |
| Commission_6 | REAL | 7 | 1 |
| Total_EC_1 | REAL | 7 | 1 |
| Total_EC_2 | REAL | 7 | 1 |
| Total_EC_3 | REAL | 7 | 1 |
| Total_EC_4 | REAL | 7 | 1 |
| Total_EC_5 | REAL | 7 | 1 |
| Total_EC_6 | REAL | 7 | 1 |
| Total_TS_1 | REAL | 7 | 1 |
| Total_TS_2 | REAL | 7 | 1 |
| Total_TS_3 | REAL | 7 | 1 |
| Total_TS_4 | REAL | 7 | 1 |
| Total_TS_5 | REAL | 7 | 1 |
| Total_TS_6 | REAL | 7 | 1 |
| Total_AS_1 | REAL | 7 | 1 |
| Total_AS_2 | REAL | 7 | 1 |
| Total_AS_3 | REAL | 7 | 1 |
| Total_AS_4 | REAL | 7 | 1 |
| Total_AS_5 | REAL | 7 | 1 |
| Total_AS_6 | REAL | 7 | 1 |
| NonRecurrNA_1 | REAL | 7 | 1 |
| NonRecurrNA_2 | REAL | 7 | 1 |
| NonRecurrNA_3 | REAL | 7 | 1 |
| NonRecurrNA_4 | REAL | 7 | 1 |
| NonRecurrNA_5 | REAL | 7 | 1 |
| NonRecurrNA_6 | REAL | 7 | 1 |
| ProfitDollars_1 | REAL | 7 | 1 |
| ProfitDollars_2 | REAL | 7 | 1 |
| ProfitDollars_3 | REAL | 7 | 1 |
| ProfitDollars_4 | REAL | 7 | 1 |
| ProfitDollars_5 | REAL | 7 | 1 |
| ProfitDollars_6 | REAL | 7 | 1 |
| ProfitPerc_1 | REAL | 7 | 1 |
| ProfitPerc_2 | REAL | 7 | 1 |
| ProfitPerc_3 | REAL | 7 | 1 |
| ProfitPerc_4 | REAL | 7 | 1 |
| ProfitPerc_5 | REAL | 7 | 1 |
| ProfitPerc_6 | REAL | 7 | 1 |
| ValueAddedPerc_1 | REAL | 7 | 1 |
| ValueAddedPerc_2 | REAL | 7 | 1 |
| ValueAddedPerc_3 | REAL | 7 | 1 |
| ValueAddedPerc_4 | REAL | 7 | 1 |
| ValueAddedPerc_5 | REAL | 7 | 1 |
| ValueAddedPerc_6 | REAL | 7 | 1 |
| Materials_MU_1 | REAL | 7 | 1 |
| Materials_MU_2 | REAL | 7 | 1 |
| Materials_MU_3 | REAL | 7 | 1 |
| Materials_MU_4 | REAL | 7 | 1 |
| Materials_MU_5 | REAL | 7 | 1 |
| Materials_MU_6 | REAL | 7 | 1 |
| Labor_MU_1 | REAL | 7 | 1 |
| Labor_MU_2 | REAL | 7 | 1 |
| Labor_MU_3 | REAL | 7 | 1 |
| Labor_MU_4 | REAL | 7 | 1 |
| Labor_MU_5 | REAL | 7 | 1 |
| Labor_MU_6 | REAL | 7 | 1 |
| Total_MU_1 | REAL | 7 | 1 |
| Total_MU_2 | REAL | 7 | 1 |
| Total_MU_3 | REAL | 7 | 1 |
| Total_MU_4 | REAL | 7 | 1 |
| Total_MU_5 | REAL | 7 | 1 |
| Total_MU_6 | REAL | 7 | 1 |
| EstGrandTotal_1 | REAL | 7 | 1 |
| EstGrandTotal_2 | REAL | 7 | 1 |
| EstGrandTotal_3 | REAL | 7 | 1 |
| EstGrandTotal_4 | REAL | 7 | 1 |
| EstGrandTotal_5 | REAL | 7 | 1 |
| EstGrandTotal_6 | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |

### Est_Tools

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| EstimateNumber | CLOB | 10 | 1 |
| RoutingNo | INT16 | 6 | 1 |
| ToolNo | CLOB | 15 | 1 |
| ToolDescr | CLOB | 20 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### Est_UserDefined

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| EquipUserDefined_ID | INT32 | 11 | 1 |
| EstimateNumber | CLOB | 10 | 1 |
| Description | CLOB | 20 | 1 |
| UseThisOption | BOOLEAN | 5 | 1 |
| Notes | CLOB | 60 | 1 |
| Print_On_Reports | BOOLEAN | 5 | 1 |
| Order_in_List | INT32 | 11 | 1 |
| Press_Number | CLOB | 10 | 1 |
| Option_Multiplier | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |

### Estimate

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| Number | CLOB | 10 | 1 |
| CustNum | CLOB | 10 | 1 |
| EndUserNum | CLOB | 10 | 1 |
| Distrubutor | BOOLEAN | 5 | 1 |
| Application | CLOB | 80 | 1 |
| Quantity1 | INT32 | 11 | 1 |
| PricePerM1 | REAL | 7 | 1 |
| TotalEst1 | REAL | 7 | 1 |
| Quantity2 | INT32 | 11 | 1 |
| PricePerM2 | REAL | 7 | 1 |
| TotalEst2 | REAL | 7 | 1 |
| Quantity3 | INT32 | 11 | 1 |
| PricePerM3 | REAL | 7 | 1 |
| TotalEst3 | REAL | 7 | 1 |
| Quantity4 | INT32 | 11 | 1 |
| PricePerM4 | REAL | 7 | 1 |
| TotalEst4 | REAL | 7 | 1 |
| Quantity5 | INT32 | 11 | 1 |
| PricePerM5 | REAL | 7 | 1 |
| TotalEst5 | REAL | 7 | 1 |
| Quantity6 | INT32 | 11 | 1 |
| PricePerM6 | REAL | 7 | 1 |
| TotalEst6 | REAL | 7 | 1 |
| NoLabAcrossFin | INT16 | 6 | 1 |
| NewTool | BOOLEAN | 5 | 1 |
| SizeAcross | REAL | 7 | 1 |
| SizeAround | REAL | 7 | 1 |
| ColSpace | REAL | 7 | 1 |
| RowSpace | REAL | 7 | 1 |
| NoAcross | INT16 | 6 | 1 |
| NoAround | INT16 | 6 | 1 |
| Shape | CLOB | 40 | 1 |
| LabelRepeat | REAL | 7 | 1 |
| CornerRadius | REAL | 7 | 1 |
| CarrierWidth | REAL | 7 | 1 |
| NoColors | INT16 | 6 | 1 |
| NoFloods | INT16 | 6 | 1 |
| ColorDescr | CLOB | 80 | 1 |
| PressNum | CLOB | 10 | 1 |
| TurnBar | BOOLEAN | 5 | 1 |
| Pinfeed | BOOLEAN | 5 | 1 |
| ConsecNo | BOOLEAN | 5 | 1 |
| CSACert | BOOLEAN | 5 | 1 |
| FinishType | CLOB | 10 | 1 |
| LabelsPer_ | INT32 | 11 | 1 |
| ColumnPerf | REAL | 7 | 1 |
| RowPerf | REAL | 7 | 1 |
| ToolSize | REAL | 7 | 1 |
| Steel | CLOB | 15 | 1 |
| NoPlateRolls | INT16 | 6 | 1 |
| ToolOverride | REAL | 7 | 1 |
| ToolTotal | REAL | 7 | 1 |
| NoColorChange | INT16 | 6 | 1 |
| NoPlateChange | INT16 | 6 | 1 |
| NewPlates | BOOLEAN | 5 | 1 |
| PlateOveride | REAL | 7 | 1 |
| PlateTotal | REAL | 7 | 1 |
| Margin | REAL | 7 | 1 |
| MiscChargeDesc | CLOB | 80 | 1 |
| MiscCharge | REAL | 7 | 1 |
| AdditionalDescr | CLOB | 80 | 1 |
| StockNum1 | CLOB | 10 | 1 |
| StockWidth1 | REAL | 7 | 1 |
| StockNum2 | CLOB | 10 | 1 |
| StockWidth2 | REAL | 7 | 1 |
| StockNum3 | CLOB | 10 | 1 |
| StockWidth3 | REAL | 7 | 1 |
| DistributorNum | CLOB | 10 | 1 |
| OTSAssocNum | CLOB | 10 | 1 |
| EstimatorsNotes | CLOB | 0 | 1 |
| ITSNum | CLOB | 10 | 1 |
| CustName | CLOB | 80 | 1 |
| EstDate | TIMESTAMP | 19 | 1 |
| ToolNo1 | CLOB | 15 | 1 |
| ToolNo2 | CLOB | 15 | 1 |
| Tool2Descr | CLOB | 20 | 1 |
| ToolNo3 | CLOB | 15 | 1 |
| Tool3Descr | CLOB | 20 | 1 |
| ToolNo4 | CLOB | 15 | 1 |
| Tool4Descr | CLOB | 20 | 1 |
| ToolNo5 | CLOB | 15 | 1 |
| Tool5Descr | CLOB | 20 | 1 |
| ProdGroup | CLOB | 40 | 1 |
| LabelsPerFold | INT16 | 6 | 1 |
| SheetPackType | CLOB | 15 | 1 |
| Tab | REAL | 7 | 1 |
| StockDescr1 | CLOB | 80 | 1 |
| StockDescr2 | CLOB | 80 | 1 |
| StockDescr3 | CLOB | 80 | 1 |
| PressSP1 | INT16 | 6 | 1 |
| PressSPCalc1 | INT16 | 6 | 1 |
| PressSP2 | INT16 | 6 | 1 |
| PressSPCalc2 | INT16 | 6 | 1 |
| PressSP3 | INT16 | 6 | 1 |
| PressSPCalc3 | INT16 | 6 | 1 |
| PressSP4 | INT16 | 6 | 1 |
| PressSPCalc4 | INT16 | 6 | 1 |
| PressSP5 | INT16 | 6 | 1 |
| PressSPCalc5 | INT16 | 6 | 1 |
| PressSP6 | INT16 | 6 | 1 |
| PressSPCalc6 | INT16 | 6 | 1 |
| PlateChangeCost | REAL | 7 | 1 |
| ColorChangeCost | REAL | 7 | 1 |
| JobOut1 | REAL | 7 | 1 |
| JobOut2 | REAL | 7 | 1 |
| JobOut3 | REAL | 7 | 1 |
| JobOut4 | REAL | 7 | 1 |
| JobOut5 | REAL | 7 | 1 |
| JobOut6 | REAL | 7 | 1 |
| PlateChangeAction | CLOB | 20 | 1 |
| ColorChangeAction | CLOB | 20 | 1 |
| ArtCharge | REAL | 7 | 1 |
| Art_Display | BOOLEAN | 5 | 1 |
| EstDraw | BLOB | 0 | 1 |
| AltMargin | REAL | 7 | 1 |
| StockFactor | REAL | 7 | 1 |
| InkFactor | REAL | 7 | 1 |
| FinishFactor | REAL | 7 | 1 |
| WrapFactor | REAL | 7 | 1 |
| MakeRedFactor | REAL | 7 | 1 |
| TabPosition | BOOLEAN | 5 | 1 |
| EndUserName | CLOB | 80 | 1 |
| LaminateMSI | REAL | 7 | 1 |
| FaceStockMSI | REAL | 7 | 1 |
| AdhesiveMSI | REAL | 7 | 1 |
| UVCoating | BOOLEAN | 5 | 1 |
| CustContact | CLOB | 40 | 1 |
| CustIsDist | BOOLEAN | 5 | 1 |
| SlitOnRewind | BOOLEAN | 5 | 1 |
| CoreSize | REAL | 7 | 1 |
| AutoAppl | BOOLEAN | 5 | 1 |
| FinalUnWind | CLOB | 15 | 1 |
| ULCert | BOOLEAN | 5 | 1 |
| PriceMode | CLOB | 20 | 1 |
| LetterNotes | CLOB | 0 | 1 |
| Est_Time | INTERVAL | 10 | 1 |
| AddCost1 | REAL | 7 | 1 |
| AddCost2 | REAL | 7 | 1 |
| AddCost3 | REAL | 7 | 1 |
| AddCost4 | REAL | 7 | 1 |
| AddCost5 | REAL | 7 | 1 |
| AddCost6 | REAL | 7 | 1 |
| RollLength | INT32 | 11 | 1 |
| RollUnit | CLOB | 7 | 1 |
| Tape | BOOLEAN | 5 | 1 |
| CoreFactor | REAL | 7 | 1 |
| CartonFactor | REAL | 7 | 1 |
| PackFactor | REAL | 7 | 1 |
| WashupFactor | REAL | 7 | 1 |
| MaterialMU | REAL | 7 | 1 |
| LaborMU | REAL | 7 | 1 |
| Commission | REAL | 7 | 1 |
| ProfitAdjLabel | CLOB | 20 | 1 |
| Reciprocal | BOOLEAN | 5 | 1 |
| LetterHead | BLOB | 0 | 1 |
| MatMu1 | REAL | 7 | 1 |
| MatMu2 | REAL | 7 | 1 |
| MatMu3 | REAL | 7 | 1 |
| MatMu4 | REAL | 7 | 1 |
| MatMu5 | REAL | 7 | 1 |
| MatMu6 | REAL | 7 | 1 |
| LabMu1 | REAL | 7 | 1 |
| LabMu2 | REAL | 7 | 1 |
| LabMu3 | REAL | 7 | 1 |
| LabMu4 | REAL | 7 | 1 |
| LabMu5 | REAL | 7 | 1 |
| LabMu6 | REAL | 7 | 1 |
| SalesRepName | CLOB | 60 | 1 |
| Contact_ID | CLOB | 10 | 1 |
| UserDef_MR_1 | BOOLEAN | 5 | 1 |
| UserDef_MR_2 | BOOLEAN | 5 | 1 |
| UserDef_MR_1_Lb | CLOB | 20 | 1 |
| UserDef_MR_2_Lb | CLOB | 20 | 1 |
| PressSpeedFacto | REAL | 7 | 1 |
| Caliper_Laminat | REAL | 7 | 1 |
| Caliper_FaceStk | REAL | 7 | 1 |
| Caliper_Adhesiv | REAL | 7 | 1 |
| OutsideDiameter | REAL | 7 | 1 |
| RewindEquipNum | CLOB | 10 | 1 |
| RewindEquipNam | CLOB | 35 | 1 |
| PrintInkType | CLOB | 20 | 1 |
| FloodInkType | CLOB | 20 | 1 |
| AmortizeToolCost | BOOLEAN | 5 | 1 |
| AmortizePlateCost | BOOLEAN | 5 | 1 |
| AmortizeArtCost | BOOLEAN | 5 | 1 |
| ITS_Name | CLOB | 35 | 1 |
| WonLostStatus | CLOB | 10 | 1 |
| GroupedWithEstNum | CLOB | 10 | 1 |
| WonLostExplanation | CLOB | 80 | 1 |
| Post_Press_Notes | CLOB | 0 | 1 |
| PostPress_Factor | REAL | 7 | 1 |
| Internet_Submission | BOOLEAN | 5 | 1 |
| PrintInk_2_Type | CLOB | 20 | 1 |
| PrintInk_2_NoColors | INT16 | 6 | 1 |
| PrintInk_2_Coverage | REAL | 7 | 1 |
| PrintInk_3_Type | CLOB | 20 | 1 |
| PrintInk_3_NoColors | INT16 | 6 | 1 |
| PrintInk_3_Coverage | REAL | 7 | 1 |
| FloodInk_2_Type | CLOB | 20 | 1 |
| FloodInk_2_NoColors | INT16 | 6 | 1 |
| FloodInk_2_Coverage | REAL | 7 | 1 |
| FloodInk_3_Type | CLOB | 20 | 1 |
| FloodInk_3_NoColors | INT16 | 6 | 1 |
| FloodInk_3_Coverage | REAL | 7 | 1 |
| PrintInk_1_Coverage | REAL | 7 | 1 |
| FloodInk_1_Coverage | REAL | 7 | 1 |
| PrintInk_1_NoColors | INT16 | 6 | 1 |
| FloodInk_1_NoColors | INT16 | 6 | 1 |
| StockNotes | CLOB | 0 | 1 |
| Sheet_Width | REAL | 7 | 1 |
| Sheet_Height | REAL | 7 | 1 |
| EnteredBy | CLOB | 50 | 1 |
| EnteredDate | TIMESTAMP | 19 | 1 |
| EnteredTime | INTERVAL | 10 | 1 |
| ModifiedBy | CLOB | 50 | 1 |
| ModifiedDate | TIMESTAMP | 19 | 1 |
| ModifiedTime | INTERVAL | 10 | 1 |
| Equip_ID | CLOB | 10 | 1 |
| Are_Tools_for_Equip | BOOLEAN | 5 | 1 |
| Eq_PrintInk_1_Type | CLOB | 20 | 1 |
| Eq_PrintInk_1_NoColors | INT16 | 6 | 1 |
| Eq_PrintInk_1_Coverage | REAL | 7 | 1 |
| Eq_FloodInk_1_Type | CLOB | 20 | 1 |
| Eq_FloodInk_1_NoColors | INT16 | 6 | 1 |
| Eq_FloodInk_1_Coverage | REAL | 7 | 1 |
| Eq_ColorDescr | CLOB | 40 | 1 |
| Equip_Speed_1 | INT16 | 6 | 1 |
| Equip_Speed_2 | INT16 | 6 | 1 |
| Equip_Speed_3 | INT16 | 6 | 1 |
| Equip_Speed_4 | INT16 | 6 | 1 |
| Equip_Speed_5 | INT16 | 6 | 1 |
| Equip_Speed_6 | INT16 | 6 | 1 |
| Equip_AltSpeed_1 | INT16 | 6 | 1 |
| Equip_AltSpeed_2 | INT16 | 6 | 1 |
| Equip_AltSpeed_3 | INT16 | 6 | 1 |
| Equip_AltSpeed_4 | INT16 | 6 | 1 |
| Equip_AltSpeed_5 | INT16 | 6 | 1 |
| Equip_AltSpeed_6 | INT16 | 6 | 1 |
| Equip_InkFactor | REAL | 7 | 1 |
| Equip_SpeedFactor | REAL | 7 | 1 |
| Equip_MakeReadyFactor | REAL | 7 | 1 |
| Equip_WashUpFactor | REAL | 7 | 1 |
| ULCert_RefNum | CLOB | 20 | 1 |
| Product_Number | CLOB | 30 | 1 |
| CriticalQuality | CLOB | 0 | 1 |
| StockPrice_Laminate_1 | REAL | 7 | 1 |
| StockPrice_Laminate_2 | REAL | 7 | 1 |
| StockPrice_Laminate_3 | REAL | 7 | 1 |
| StockPrice_Laminate_4 | REAL | 7 | 1 |
| StockPrice_Laminate_5 | REAL | 7 | 1 |
| StockPrice_Laminate_6 | REAL | 7 | 1 |
| StockPrice_Base_1 | REAL | 7 | 1 |
| StockPrice_Base_2 | REAL | 7 | 1 |
| StockPrice_Base_3 | REAL | 7 | 1 |
| StockPrice_Base_4 | REAL | 7 | 1 |
| StockPrice_Base_5 | REAL | 7 | 1 |
| StockPrice_Base_6 | REAL | 7 | 1 |
| StockPrice_3rdStock_1 | REAL | 7 | 1 |
| StockPrice_3rdStock_2 | REAL | 7 | 1 |
| StockPrice_3rdStock_3 | REAL | 7 | 1 |
| StockPrice_3rdStock_4 | REAL | 7 | 1 |
| StockPrice_3rdStock_5 | REAL | 7 | 1 |
| StockPrice_3rdStock_6 | REAL | 7 | 1 |
| New_Plate_Count | INT32 | 11 | 1 |
| Are_NewPlates_Entered | BOOLEAN | 5 | 1 |
| FreightCost_1 | REAL | 7 | 1 |
| FreightCost_2 | REAL | 7 | 1 |
| FreightCost_3 | REAL | 7 | 1 |
| FreightCost_4 | REAL | 7 | 1 |
| FreightCost_5 | REAL | 7 | 1 |
| FreightCost_6 | REAL | 7 | 1 |
| FreightCost_User | INT32 | 11 | 1 |
| LaminateMSI_Override | BOOLEAN | 5 | 1 |
| FaceStockMSI_Override | BOOLEAN | 5 | 1 |
| AdhesiveMSI_Override | BOOLEAN | 5 | 1 |
| HighestQuantity | INT32 | 11 | 1 |
| InternetQuery | BOOLEAN | 5 | 1 |
| HighestTotalDollars | REAL | 7 | 1 |
| Press_Null_Cycles | INT32 | 11 | 1 |
| Equip_Null_Cycles | INT32 | 11 | 1 |
| CompareTo_EstimateNumber | CLOB | 10 | 1 |
| Time_RoundTo_Digits | INT32 | 11 | 1 |
| Use_TurretRewinder | BOOLEAN | 5 | 1 |
| Currency_ID | INT32 | 11 | 1 |
| Currency_ExchangeRate | REAL | 7 | 1 |
| NoAround_PrintCylinder | INT32 | 11 | 1 |
| Is_InkCoverage_TotalPercent | BOOLEAN | 5 | 1 |
| ShrinkSleeve_OverLap | REAL | 7 | 1 |
| ShrinkSleeve_LayFlat | REAL | 7 | 1 |
| ShrinkSleeve_CutHeight | REAL | 7 | 1 |
| CommissionSource | CLOB | 20 | 1 |
| MFGRepNumber | CLOB | 10 | 1 |
| MFGRepCommission | REAL | 7 | 1 |
| MFGRepName | CLOB | 80 | 1 |
| NoAcross_OverRide | BOOLEAN | 5 | 1 |
| NoAround_OverRide | BOOLEAN | 5 | 1 |
| Equip3_ID | CLOB | 10 | 1 |
| Equip3_PrintInk_1_Type | CLOB | 20 | 1 |
| Equip3_PrintInk_1_NoColors | INT16 | 6 | 1 |
| Equip3_PrintInk_1_Coverage | REAL | 7 | 1 |
| Equip3_FloodInk_1_Type | CLOB | 20 | 1 |
| Equip3_FloodInk_1_NoColors | INT16 | 6 | 1 |
| Equip3_FloodInk_1_Coverage | REAL | 7 | 1 |
| Equip3_ColorDescr | CLOB | 40 | 1 |
| Equip3_Speed_1 | INT16 | 6 | 1 |
| Equip3_Speed_2 | INT16 | 6 | 1 |
| Equip3_Speed_3 | INT16 | 6 | 1 |
| Equip3_Speed_4 | INT16 | 6 | 1 |
| Equip3_Speed_5 | INT16 | 6 | 1 |
| Equip3_Speed_6 | INT16 | 6 | 1 |
| Equip3_AltSpeed_1 | INT16 | 6 | 1 |
| Equip3_AltSpeed_2 | INT16 | 6 | 1 |
| Equip3_AltSpeed_3 | INT16 | 6 | 1 |
| Equip3_AltSpeed_4 | INT16 | 6 | 1 |
| Equip3_AltSpeed_5 | INT16 | 6 | 1 |
| Equip3_AltSpeed_6 | INT16 | 6 | 1 |
| Equip3_InkFactor | REAL | 7 | 1 |
| Equip3_SpeedFactor | REAL | 7 | 1 |
| Equip3_MakeReadyFactor | REAL | 7 | 1 |
| Equip3_WashUpFactor | REAL | 7 | 1 |
| Equip3_Null_Cycles | INT32 | 11 | 1 |
| Equip4_ID | CLOB | 10 | 1 |
| Equip4_PrintInk_1_Type | CLOB | 20 | 1 |
| Equip4_PrintInk_1_NoColors | INT16 | 6 | 1 |
| Equip4_PrintInk_1_Coverage | REAL | 7 | 1 |
| Equip4_FloodInk_1_Type | CLOB | 20 | 1 |
| Equip4_FloodInk_1_NoColors | INT16 | 6 | 1 |
| Equip4_FloodInk_1_Coverage | REAL | 7 | 1 |
| Equip4_ColorDescr | CLOB | 40 | 1 |
| Equip4_Speed_1 | INT16 | 6 | 1 |
| Equip4_Speed_2 | INT16 | 6 | 1 |
| Equip4_Speed_3 | INT16 | 6 | 1 |
| Equip4_Speed_4 | INT16 | 6 | 1 |
| Equip4_Speed_5 | INT16 | 6 | 1 |
| Equip4_Speed_6 | INT16 | 6 | 1 |
| Equip4_AltSpeed_1 | INT16 | 6 | 1 |
| Equip4_AltSpeed_2 | INT16 | 6 | 1 |
| Equip4_AltSpeed_3 | INT16 | 6 | 1 |
| Equip4_AltSpeed_4 | INT16 | 6 | 1 |
| Equip4_AltSpeed_5 | INT16 | 6 | 1 |
| Equip4_AltSpeed_6 | INT16 | 6 | 1 |
| Equip4_InkFactor | REAL | 7 | 1 |
| Equip4_SpeedFactor | REAL | 7 | 1 |
| Equip4_MakeReadyFactor | REAL | 7 | 1 |
| Equip4_WashUpFactor | REAL | 7 | 1 |
| Equip4_Null_Cycles | INT32 | 11 | 1 |
| Equip_NoAcross | INT32 | 11 | 1 |
| Equip_NoAround | INT32 | 11 | 1 |
| Equip_NumUp_Multiplier | INT32 | 11 | 1 |
| Equip3_NoAcross | INT32 | 11 | 1 |
| Equip3_NoAround | INT32 | 11 | 1 |
| Equip3_NumUp_Multiplier | INT32 | 11 | 1 |
| Equip4_NoAcross | INT32 | 11 | 1 |
| Equip4_NoAround | INT32 | 11 | 1 |
| Equip4_NumUp_Multiplier | INT32 | 11 | 1 |
| Tool_NumberAround | INT16 | 6 | 1 |
| Roto_Prod_Fam_Type | CLOB | 20 | 1 |
| Roto_CavityShap_Code | CLOB | 20 | 1 |
| Roto_NonStickText | CLOB | 20 | 1 |
| Roto_DrillShaft_Code | CLOB | 20 | 1 |
| Roto_NumHolesCavity | CLOB | 20 | 1 |
| Roto_Treatment_Code | CLOB | 20 | 1 |
| Roto_CutType_Code | CLOB | 20 | 1 |
| Roto_LayoutOpt_Code | CLOB | 20 | 1 |
| Roto_CutPosition_Code | CLOB | 20 | 1 |
| Roto_LabelAppl_Code | CLOB | 20 | 1 |
| Roto_PatternCentered | CLOB | 20 | 1 |
| Roto_BladeHeightSel_Code | CLOB | 20 | 1 |
| Roto_Quote_Number | CLOB | 80 | 1 |
| Roto_Quote_Line_ID | CLOB | 80 | 1 |
| Roto_Quote_Status | CLOB | 80 | 1 |
| Roto_Num_Perf_Sets | CLOB | 20 | 1 |
| Roto_SpecialBladeHeight | CLOB | 20 | 1 |
| Tool_BasePrice | REAL | 7 | 1 |
| Tool_Freight | REAL | 7 | 1 |
| Tool_MarkUp | REAL | 7 | 1 |
| Tool_PrintRollTotal | REAL | 7 | 1 |
| Roto_CEL_Product_ID | CLOB | 20 | 1 |
| aLC_Equip_White_Count | INT32 | 11 | 1 |
| aLC_Equip_White_Coverage | REAL | 7 | 1 |
| aLC_Equip3_White_Count | INT32 | 11 | 1 |
| aLC_Equip3_White_Coverage | REAL | 7 | 1 |
| aLC_Equip4_White_Count | INT32 | 11 | 1 |
| aLC_Equip4_White_Coverage | REAL | 7 | 1 |
| PP_Total_PressCost1 | REAL | 7 | 1 |
| PP_Amort_Cost1 | REAL | 7 | 1 |
| PP_Finish_Hours1 | REAL | 7 | 1 |
| PP_Finish_Cost1 | REAL | 7 | 1 |
| PP_Wrap_Cost1 | REAL | 7 | 1 |
| PP_Core_Cost1 | REAL | 7 | 1 |
| PP_Stock_Cost1 | REAL | 7 | 1 |
| PP_Total_InkCost1 | REAL | 7 | 1 |
| PP_Total_PressHours1 | REAL | 7 | 1 |
| PP_Weight1 | REAL | 7 | 1 |
| PP_Carton_Cost1 | REAL | 7 | 1 |
| PP_Packaging_Cost1 | REAL | 7 | 1 |
| PP_PostPress_Total1 | REAL | 7 | 1 |
| PP_Finish_Cost2 | REAL | 7 | 1 |
| PP_Stock_Cost2 | REAL | 7 | 1 |
| PP_PostPress_Total2 | REAL | 7 | 1 |
| PP_Total_InkCost2 | REAL | 7 | 1 |
| PP_Total_PressHours2 | REAL | 7 | 1 |
| PP_Total_PressCost2 | REAL | 7 | 1 |
| PP_Amort_Cost2 | REAL | 7 | 1 |
| PP_Finish_Hours2 | REAL | 7 | 1 |
| PP_Wrap_Cost2 | REAL | 7 | 1 |
| PP_Core_Cost2 | REAL | 7 | 1 |
| PP_Weight2 | REAL | 7 | 1 |
| PP_Packaging_Cost2 | REAL | 7 | 1 |
| PP_Carton_Cost2 | REAL | 7 | 1 |
| PP_Total_PressCost3 | REAL | 7 | 1 |
| PP_Amort_Cost3 | REAL | 7 | 1 |
| PP_Finish_Hours3 | REAL | 7 | 1 |
| PP_Finish_Cost3 | REAL | 7 | 1 |
| PP_Wrap_Cost3 | REAL | 7 | 1 |
| PP_Core_Cost3 | REAL | 7 | 1 |
| PP_Stock_Cost3 | REAL | 7 | 1 |
| PP_Total_InkCost3 | REAL | 7 | 1 |
| PP_Total_PressHours3 | REAL | 7 | 1 |
| PP_Weight3 | REAL | 7 | 1 |
| PP_Carton_Cost3 | REAL | 7 | 1 |
| PP_Packaging_Cost3 | REAL | 7 | 1 |
| PP_PostPress_Total3 | REAL | 7 | 1 |
| PP_Total_PressCost4 | REAL | 7 | 1 |
| PP_Amort_Cost4 | REAL | 7 | 1 |
| PP_Finish_Hours4 | REAL | 7 | 1 |
| PP_Finish_Cost4 | REAL | 7 | 1 |
| PP_Wrap_Cost4 | REAL | 7 | 1 |
| PP_Core_Cost4 | REAL | 7 | 1 |
| PP_Stock_Cost4 | REAL | 7 | 1 |
| PP_Total_InkCost4 | REAL | 7 | 1 |
| PP_Total_PressHours4 | REAL | 7 | 1 |
| PP_Weight4 | REAL | 7 | 1 |
| PP_Carton_Cost4 | REAL | 7 | 1 |
| PP_Packaging_Cost4 | REAL | 7 | 1 |
| PP_PostPress_Total4 | REAL | 7 | 1 |
| PP_Total_PressCost5 | REAL | 7 | 1 |
| PP_Amort_Cost5 | REAL | 7 | 1 |
| PP_Finish_Hours5 | REAL | 7 | 1 |
| PP_Finish_Cost5 | REAL | 7 | 1 |
| PP_Wrap_Cost5 | REAL | 7 | 1 |
| PP_Core_Cost5 | REAL | 7 | 1 |
| PP_Stock_Cost5 | REAL | 7 | 1 |
| PP_Total_InkCost5 | REAL | 7 | 1 |
| PP_Total_PressHours5 | REAL | 7 | 1 |
| PP_Weight5 | REAL | 7 | 1 |
| PP_Carton_Cost5 | REAL | 7 | 1 |
| PP_Packaging_Cost5 | REAL | 7 | 1 |
| PP_PostPress_Total5 | REAL | 7 | 1 |
| PP_Total_PressCost6 | REAL | 7 | 1 |
| PP_Amort_Cost6 | REAL | 7 | 1 |
| PP_Finish_Hours6 | REAL | 7 | 1 |
| PP_Finish_Cost6 | REAL | 7 | 1 |
| PP_Wrap_Cost6 | REAL | 7 | 1 |
| PP_Core_Cost6 | REAL | 7 | 1 |
| PP_Stock_Cost6 | REAL | 7 | 1 |
| PP_Total_InkCost6 | REAL | 7 | 1 |
| PP_Total_PressHours6 | REAL | 7 | 1 |
| PP_Weight6 | REAL | 7 | 1 |
| PP_Carton_Cost6 | REAL | 7 | 1 |
| PP_Packaging_Cost6 | REAL | 7 | 1 |
| PP_PostPress_Total6 | REAL | 7 | 1 |
| PP_MakeReady_Hours | REAL | 7 | 1 |
| PP_MakeReady_Cost | REAL | 7 | 1 |
| PP_WashUp_Hours | REAL | 7 | 1 |
| PP_WashUp_Cost | REAL | 7 | 1 |
| PP_UL_CSA_AdminFee | REAL | 7 | 1 |
| PP_Artwork_Cost | REAL | 7 | 1 |
| PP_Misc_Charge | REAL | 7 | 1 |
| PP_Total_NonRecurring | REAL | 7 | 1 |
| PP_Total_Production1 | REAL | 7 | 1 |
| PP_Total_Production2 | REAL | 7 | 1 |
| PP_Total_Production3 | REAL | 7 | 1 |
| PP_Total_Production4 | REAL | 7 | 1 |
| PP_Total_Production5 | REAL | 7 | 1 |
| PP_Total_Production6 | REAL | 7 | 1 |
| Currency_Rate_ID | INT32 | 11 | 1 |
| FX_PriceFinal_1 | REAL | 7 | 1 |
| FX_PriceFinal_2 | REAL | 7 | 1 |
| FX_PriceFinal_3 | REAL | 7 | 1 |
| FX_PriceFinal_4 | REAL | 7 | 1 |
| FX_PriceFinal_5 | REAL | 7 | 1 |
| FX_PriceFinal_6 | REAL | 7 | 1 |
| FX_ArtFinal | REAL | 7 | 1 |
| FX_PlateFinal | REAL | 7 | 1 |
| FX_ToolFinal | REAL | 7 | 1 |
| FX_MiscFinal | REAL | 7 | 1 |
| FX_PlateChangeCostFinal | REAL | 7 | 1 |
| FX_ColorChangeCostFinal | REAL | 7 | 1 |
| FX_PriceTranslated_1 | REAL | 7 | 1 |
| FX_PriceTranslated_2 | REAL | 7 | 1 |
| FX_PriceTranslated_3 | REAL | 7 | 1 |
| FX_PriceTranslated_4 | REAL | 7 | 1 |
| FX_PriceTranslated_5 | REAL | 7 | 1 |
| FX_PriceTranslated_6 | REAL | 7 | 1 |
| FX_ArtTranslated | REAL | 7 | 1 |
| FX_PlateTranslated | REAL | 7 | 1 |
| FX_ToolTranslated | REAL | 7 | 1 |
| FX_MiscTranslated | REAL | 7 | 1 |
| FX_PlateChangeCostTrans | REAL | 7 | 1 |
| FX_ColorChangeCostTrans | REAL | 7 | 1 |
| FX_PriceVariance_1 | REAL | 7 | 1 |
| FX_PriceVariance_2 | REAL | 7 | 1 |
| FX_PriceVariance_3 | REAL | 7 | 1 |
| FX_PriceVariance_4 | REAL | 7 | 1 |
| FX_PriceVariance_5 | REAL | 7 | 1 |
| FX_PriceVariance_6 | REAL | 7 | 1 |
| FX_TotalEstFinal_1 | REAL | 7 | 1 |
| FX_TotalEstFinal_2 | REAL | 7 | 1 |
| FX_TotalEstFinal_3 | REAL | 7 | 1 |
| FX_TotalEstFinal_4 | REAL | 7 | 1 |
| FX_TotalEstFinal_5 | REAL | 7 | 1 |
| FX_TotalEstFinal_6 | REAL | 7 | 1 |
| FX_TotalEstTranslated_1 | REAL | 7 | 1 |
| FX_TotalEstTranslated_2 | REAL | 7 | 1 |
| FX_TotalEstTranslated_3 | REAL | 7 | 1 |
| FX_TotalEstTranslated_4 | REAL | 7 | 1 |
| FX_TotalEstTranslated_5 | REAL | 7 | 1 |
| FX_TotalEstTranslated_6 | REAL | 7 | 1 |
| FX_TotalEstVariance_1 | REAL | 7 | 1 |
| FX_TotalEstVariance_2 | REAL | 7 | 1 |
| FX_TotalEstVariance_3 | REAL | 7 | 1 |
| FX_TotalEstVariance_4 | REAL | 7 | 1 |
| FX_TotalEstVariance_5 | REAL | 7 | 1 |
| FX_TotalEstVariance_6 | REAL | 7 | 1 |
| FX_PriceFinalOverride_1 | BOOLEAN | 5 | 1 |
| FX_PriceFinalOverride_2 | BOOLEAN | 5 | 1 |
| FX_PriceFinalOverride_3 | BOOLEAN | 5 | 1 |
| FX_PriceFinalOverride_4 | BOOLEAN | 5 | 1 |
| FX_PriceFinalOverride_5 | BOOLEAN | 5 | 1 |
| FX_PriceFinalOverride_6 | BOOLEAN | 5 | 1 |
| FX_ArtFinalOverride | BOOLEAN | 5 | 1 |
| FX_PlateFinalOverride | BOOLEAN | 5 | 1 |
| FX_ToolFinalOverride | BOOLEAN | 5 | 1 |
| FX_MiscFinalOverride | BOOLEAN | 5 | 1 |
| FX_PlateChangeCostOverride | BOOLEAN | 5 | 1 |
| FX_ColorChangeCostOverride | BOOLEAN | 5 | 1 |
| FX_ArtTranslatedPlusMU | REAL | 7 | 1 |
| FX_ArtFinalPlusMU | REAL | 7 | 1 |
| WonLostStatus_Local | CLOB | 255 | 1 |
| PriceMode_Local | CLOB | 20 | 1 |
| RollUnit_Local | CLOB | 0 | 1 |
| CommissionSource_Local | CLOB | 0 | 1 |
| HP_Indigo_Equip4_Is_EPM | BOOLEAN | 5 | 1 |
| HP_Indigo_Press_Is_EPM | BOOLEAN | 5 | 1 |
| HP_Indigo_Equip2_Is_EPM | BOOLEAN | 5 | 1 |
| HP_Indigo_Equip3_Is_EPM | BOOLEAN | 5 | 1 |
| Is_LabelSize_InkCoverage_Press | BOOLEAN | 5 | 1 |
| Is_LabelSize_InkCoverage_Eq2 | BOOLEAN | 5 | 1 |
| Is_LabelSize_InkCoverage_Eq3 | BOOLEAN | 5 | 1 |
| Is_LabelSize_InkCoverage_Eq4 | BOOLEAN | 5 | 1 |
| MiscChargeDesc1 | CLOB | 0 | 1 |
| MiscChargeDesc2 | CLOB | 0 | 1 |
| MiscChargeDesc3 | CLOB | 0 | 1 |
| MiscChargeDesc4 | CLOB | 0 | 1 |
| MiscCharge1 | REAL | 7 | 1 |
| MiscCharge2 | REAL | 7 | 1 |
| MiscCharge3 | REAL | 7 | 1 |
| MiscCharge4 | REAL | 7 | 1 |
| FX_MiscTranslated1 | REAL | 7 | 1 |
| FX_MiscTranslated2 | REAL | 7 | 1 |
| FX_MiscTranslated3 | REAL | 7 | 1 |
| FX_MiscTranslated4 | REAL | 7 | 1 |
| FX_MiscFinal1 | REAL | 7 | 1 |
| FX_MiscFinal2 | REAL | 7 | 1 |
| FX_MiscFinal3 | REAL | 7 | 1 |
| FX_MiscFinal4 | REAL | 7 | 1 |
| Complexity_Level | INT32 | 11 | 1 |
| Converted_By | CLOB | 50 | 1 |
| Converted_Date | TIMESTAMP | 19 | 1 |
| Converted_Time | INTERVAL | 10 | 1 |
| InLinePriming_State | INT16 | 6 | 1 |
| InLinePriming_Rate | REAL | 7 | 1 |
| Roto_DieUse_Code | CLOB | 0 | 1 |
| Roto_Laser_Harden | BOOLEAN | 5 | 1 |
| Roto_Plate_Length | REAL | 7 | 1 |
| Roto_Plate_Width | REAL | 7 | 1 |
| Roto_SetPageAndPop | CLOB | 0 | 1 |
| Roto_Plate_Height | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |
| FlexPack_Height | REAL | 7 | 1 |
| FlexPack_Gusset | REAL | 7 | 1 |
| FlexPack_LeftTrim | REAL | 7 | 1 |
| FlexPack_RightTrim | REAL | 7 | 1 |
| OrderWeight1 | REAL | 7 | 1 |
| OrderWeight2 | REAL | 7 | 1 |
| OrderWeight3 | REAL | 7 | 1 |
| OrderWeight4 | REAL | 7 | 1 |
| OrderWeight5 | REAL | 7 | 1 |
| OrderWeight6 | REAL | 7 | 1 |
| FlexPack_Type | INT32 | 11 | 1 |
| Press_NewPlateCount | INT32 | 11 | 1 |
| Equip_NewPlateCount | INT32 | 11 | 1 |
| Equip3_NewPlateCount | INT32 | 11 | 1 |
| Equip4_NewPlateCount | INT32 | 11 | 1 |
| PlateChangeAction_Local | CLOB | 40 | 1 |
| ColorChangeAction_Local | CLOB | 40 | 1 |
| IsPrintReversed | BOOLEAN | 5 | 1 |
| FPUD_Popup1 | CLOB | 40 | 1 |
| FPUD_Popup2 | CLOB | 40 | 1 |
| FPUD_Popup3 | CLOB | 40 | 1 |
| FPUD_Popup4 | CLOB | 40 | 1 |
| FPUD_Popup5 | CLOB | 40 | 1 |
| FPUD_Popup6 | CLOB | 40 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |
| Est_Duration | INT32 | 11 | 1 |
| EstDuration_Status | CLOB | 20 | 1 |
| Tag | CLOB | 3 | 1 |
| Equip5_AltSpeed_1 | INT16 | 6 | 1 |
| Equip5_AltSpeed_2 | INT16 | 6 | 1 |
| Equip5_AltSpeed_3 | INT16 | 6 | 1 |
| Equip5_AltSpeed_4 | INT16 | 6 | 1 |
| Equip5_AltSpeed_5 | INT16 | 6 | 1 |
| Equip5_AltSpeed_6 | INT16 | 6 | 1 |
| Equip5_ColorDescr | CLOB | 40 | 1 |
| Equip5_FloodInk_1_Coverage | REAL | 7 | 1 |
| Equip5_FloodInk_1_NoColors | INT16 | 6 | 1 |
| Equip5_FloodInk_1_Type | CLOB | 20 | 1 |
| Equip5_ID | CLOB | 10 | 1 |
| Equip5_InkFactor | REAL | 7 | 1 |
| Equip5_MakeReadyFactor | REAL | 7 | 1 |
| Equip5_NewPlateCount | INT32 | 11 | 1 |
| Equip5_NoAcross | INT32 | 11 | 1 |
| Equip5_NoAround | INT32 | 11 | 1 |
| Equip5_Null_Cycles | INT32 | 11 | 1 |
| Equip5_NumUp_Multiplier | INT32 | 11 | 1 |
| Equip5_PrintInk_1_Coverage | REAL | 7 | 1 |
| Equip5_PrintInk_1_NoColors | INT16 | 6 | 1 |
| Equip5_PrintInk_1_Type | CLOB | 20 | 1 |
| Equip5_Speed_1 | INT16 | 6 | 1 |
| Equip5_Speed_2 | INT16 | 6 | 1 |
| Equip5_Speed_3 | INT16 | 6 | 1 |
| Equip5_Speed_4 | INT16 | 6 | 1 |
| Equip5_Speed_5 | INT16 | 6 | 1 |
| Equip5_Speed_6 | INT16 | 6 | 1 |
| Equip5_SpeedFactor | REAL | 7 | 1 |
| Equip5_WashUpFactor | REAL | 7 | 1 |
| aLC_Equip5_White_Count | INT32 | 11 | 1 |
| aLC_Equip5_White_Coverage | REAL | 7 | 1 |
| HP_Indigo_Equip5_Is_EPM | BOOLEAN | 5 | 1 |
| Is_LabelSize_InkCoverage_Eq5 | BOOLEAN | 5 | 1 |
| Equip6_AltSpeed_1 | INT16 | 6 | 1 |
| Equip6_AltSpeed_2 | INT16 | 6 | 1 |
| Equip6_AltSpeed_3 | INT16 | 6 | 1 |
| Equip6_AltSpeed_4 | INT16 | 6 | 1 |
| Equip6_AltSpeed_5 | INT16 | 6 | 1 |
| Equip6_AltSpeed_6 | INT16 | 6 | 1 |
| Equip6_ColorDescr | CLOB | 40 | 1 |
| Equip6_FloodInk_1_Coverage | REAL | 7 | 1 |
| Equip6_FloodInk_1_NoColors | INT16 | 6 | 1 |
| Equip6_FloodInk_1_Type | CLOB | 20 | 1 |
| Equip6_ID | CLOB | 10 | 1 |
| Equip6_InkFactor | REAL | 7 | 1 |
| Equip6_MakeReadyFactor | REAL | 7 | 1 |
| Equip6_NewPlateCount | INT32 | 11 | 1 |
| Equip6_NoAcross | INT32 | 11 | 1 |
| Equip6_NoAround | INT32 | 11 | 1 |
| Equip6_Null_Cycles | INT32 | 11 | 1 |
| Equip6_NumUp_Multiplier | INT32 | 11 | 1 |
| Equip6_PrintInk_1_Coverage | REAL | 7 | 1 |
| Equip6_PrintInk_1_NoColors | INT16 | 6 | 1 |
| Equip6_PrintInk_1_Type | CLOB | 20 | 1 |
| Equip6_Speed_1 | INT16 | 6 | 1 |
| Equip6_Speed_2 | INT16 | 6 | 1 |
| Equip6_Speed_3 | INT16 | 6 | 1 |
| Equip6_Speed_4 | INT16 | 6 | 1 |
| Equip6_Speed_5 | INT16 | 6 | 1 |
| Equip6_Speed_6 | INT16 | 6 | 1 |
| Equip6_SpeedFactor | REAL | 7 | 1 |
| Equip6_WashUpFactor | REAL | 7 | 1 |
| aLC_Equip6_White_Count | INT32 | 11 | 1 |
| aLC_Equip6_White_Coverage | REAL | 7 | 1 |
| HP_Indigo_Equip6_Is_EPM | BOOLEAN | 5 | 1 |
| Is_LabelSize_InkCoverage_Eq6 | BOOLEAN | 5 | 1 |
| PrintInkType_Eq2 | CLOB | 20 | 1 |
| PrintInk1Coverage_Eq2 | REAL | 7 | 1 |
| PrintInk2Type_Eq2 | CLOB | 20 | 1 |
| PrintInk2Coverage_Eq2 | REAL | 7 | 1 |
| PrintInk3Type_Eq2 | CLOB | 20 | 1 |
| PrintInk3Coverage_Eq2 | REAL | 7 | 1 |
| PrintInk1NoColors_Eq2 | INT16 | 6 | 1 |
| PrintInk2NoColors_Eq2 | INT16 | 6 | 1 |
| PrintInk3NoColors_Eq2 | INT16 | 6 | 1 |
| NoColors_Eq2 | INT16 | 6 | 1 |
| ColorDescr_Eq2 | CLOB | 80 | 1 |
| Is_LabelSizeInkCov_Press_Eq2 | BOOLEAN | 5 | 1 |
| FloodInkType_Eq2 | CLOB | 20 | 1 |
| FloodInk1Coverage_Eq2 | REAL | 7 | 1 |
| FloodInk2Type_Eq2 | CLOB | 20 | 1 |
| FloodInk2Coverage_Eq2 | REAL | 7 | 1 |
| FloodInk3Type_Eq2 | CLOB | 20 | 1 |
| FloodInk3Coverage_Eq2 | REAL | 7 | 1 |
| FloodInk1NoColors_Eq2 | INT16 | 6 | 1 |
| FloodInk2NoColors_Eq2 | INT16 | 6 | 1 |
| FloodInk3NoColors_Eq2 | INT16 | 6 | 1 |
| NoFloods_Eq2 | INT16 | 6 | 1 |
| NoAround_PrintCylinder_Eq2 | INT32 | 11 | 1 |
| NoPlateChange_Eq2 | INT16 | 6 | 1 |
| PlateChangeCost_Eq2 | REAL | 7 | 1 |
| PlateChangeActionLocal_Eq2 | CLOB | 40 | 1 |
| PlateChangeAction_Eq2 | CLOB | 20 | 1 |
| NoColorChange_Eq2 | INT16 | 6 | 1 |
| ColorChangeCost_Eq2 | REAL | 7 | 1 |
| ColorChangeActionLocal_Eq2 | CLOB | 40 | 1 |
| ColorChangeAction_Eq2 | CLOB | 20 | 1 |
| PrintInkType_Eq3 | CLOB | 20 | 1 |
| PrintInk1Coverage_Eq3 | REAL | 7 | 1 |
| PrintInk2Type_Eq3 | CLOB | 20 | 1 |
| PrintInk2Coverage_Eq3 | REAL | 7 | 1 |
| PrintInk3Type_Eq3 | CLOB | 20 | 1 |
| PrintInk3Coverage_Eq3 | REAL | 7 | 1 |
| PrintInk1NoColors_Eq3 | INT16 | 6 | 1 |
| PrintInk2NoColors_Eq3 | INT16 | 6 | 1 |
| PrintInk3NoColors_Eq3 | INT16 | 6 | 1 |
| NoColors_Eq3 | INT16 | 6 | 1 |
| ColorDescr_Eq3 | CLOB | 80 | 1 |
| Is_LabelSizeInkCov_Press_Eq3 | BOOLEAN | 5 | 1 |
| FloodInkType_Eq3 | CLOB | 20 | 1 |
| FloodInk1Coverage_Eq3 | REAL | 7 | 1 |
| FloodInk2Type_Eq3 | CLOB | 20 | 1 |
| FloodInk2Coverage_Eq3 | REAL | 7 | 1 |
| FloodInk3Type_Eq3 | CLOB | 20 | 1 |
| FloodInk3Coverage_Eq3 | REAL | 7 | 1 |
| FloodInk1NoColors_Eq3 | INT16 | 6 | 1 |
| FloodInk2NoColors_Eq3 | INT16 | 6 | 1 |
| FloodInk3NoColors_Eq3 | INT16 | 6 | 1 |
| NoFloods_Eq3 | INT16 | 6 | 1 |
| NoAround_PrintCylinder_Eq3 | INT32 | 11 | 1 |
| NoPlateChange_Eq3 | INT16 | 6 | 1 |
| PlateChangeCost_Eq3 | REAL | 7 | 1 |
| PlateChangeActionLocal_Eq3 | CLOB | 40 | 1 |
| PlateChangeAction_Eq3 | CLOB | 20 | 1 |
| NoColorChange_Eq3 | INT16 | 6 | 1 |
| ColorChangeCost_Eq3 | REAL | 7 | 1 |
| ColorChangeActionLocal_Eq3 | CLOB | 40 | 1 |
| ColorChangeAction_Eq3 | CLOB | 20 | 1 |
| PrintInkType_Eq4 | CLOB | 20 | 1 |
| PrintInk1Coverage_Eq4 | REAL | 7 | 1 |
| PrintInk2Type_Eq4 | CLOB | 20 | 1 |
| PrintInk2Coverage_Eq4 | REAL | 7 | 1 |
| PrintInk3Type_Eq4 | CLOB | 20 | 1 |
| PrintInk3Coverage_Eq4 | REAL | 7 | 1 |
| PrintInk1NoColors_Eq4 | INT16 | 6 | 1 |
| PrintInk2NoColors_Eq4 | INT16 | 6 | 1 |
| PrintInk3NoColors_Eq4 | INT16 | 6 | 1 |
| NoColors_Eq4 | INT16 | 6 | 1 |
| ColorDescr_Eq4 | CLOB | 80 | 1 |
| Is_LabelSizeInkCov_Press_Eq4 | BOOLEAN | 5 | 1 |
| FloodInkType_Eq4 | CLOB | 20 | 1 |
| FloodInk1Coverage_Eq4 | REAL | 7 | 1 |
| FloodInk2Type_Eq4 | CLOB | 20 | 1 |
| FloodInk2Coverage_Eq4 | REAL | 7 | 1 |
| FloodInk3Type_Eq4 | CLOB | 20 | 1 |
| FloodInk3Coverage_Eq4 | REAL | 7 | 1 |
| FloodInk1NoColors_Eq4 | INT16 | 6 | 1 |
| FloodInk2NoColors_Eq4 | INT16 | 6 | 1 |
| FloodInk3NoColors_Eq4 | INT16 | 6 | 1 |
| NoFloods_Eq4 | INT16 | 6 | 1 |
| NoAround_PrintCylinder_Eq4 | INT32 | 11 | 1 |
| NoPlateChange_Eq4 | INT16 | 6 | 1 |
| PlateChangeCost_Eq4 | REAL | 7 | 1 |
| PlateChangeActionLocal_Eq4 | CLOB | 40 | 1 |
| PlateChangeAction_Eq4 | CLOB | 20 | 1 |
| NoColorChange_Eq4 | INT16 | 6 | 1 |
| ColorChangeCost_Eq4 | REAL | 7 | 1 |
| ColorChangeActionLocal_Eq4 | CLOB | 40 | 1 |
| ColorChangeAction_Eq4 | CLOB | 20 | 1 |
| PrintInkType_Eq5 | CLOB | 20 | 1 |
| PrintInk1Coverage_Eq5 | REAL | 7 | 1 |
| PrintInk2Type_Eq5 | CLOB | 20 | 1 |
| PrintInk2Coverage_Eq5 | REAL | 7 | 1 |
| PrintInk3Type_Eq5 | CLOB | 20 | 1 |
| PrintInk3Coverage_Eq5 | REAL | 7 | 1 |
| PrintInk1NoColors_Eq5 | INT16 | 6 | 1 |
| PrintInk2NoColors_Eq5 | INT16 | 6 | 1 |
| PrintInk3NoColors_Eq5 | INT16 | 6 | 1 |
| NoColors_Eq5 | INT16 | 6 | 1 |
| ColorDescr_Eq5 | CLOB | 80 | 1 |
| Is_LabelSizeInkCov_Press_Eq5 | BOOLEAN | 5 | 1 |
| FloodInkType_Eq5 | CLOB | 20 | 1 |
| FloodInk1Coverage_Eq5 | REAL | 7 | 1 |
| FloodInk2Type_Eq5 | CLOB | 20 | 1 |
| FloodInk2Coverage_Eq5 | REAL | 7 | 1 |
| FloodInk3Type_Eq5 | CLOB | 20 | 1 |
| FloodInk3Coverage_Eq5 | REAL | 7 | 1 |
| FloodInk1NoColors_Eq5 | INT16 | 6 | 1 |
| FloodInk2NoColors_Eq5 | INT16 | 6 | 1 |
| FloodInk3NoColors_Eq5 | INT16 | 6 | 1 |
| NoFloods_Eq5 | INT16 | 6 | 1 |
| NoAround_PrintCylinder_Eq5 | INT32 | 11 | 1 |
| NoPlateChange_Eq5 | INT16 | 6 | 1 |
| PlateChangeCost_Eq5 | REAL | 7 | 1 |
| PlateChangeActionLocal_Eq5 | CLOB | 40 | 1 |
| PlateChangeAction_Eq5 | CLOB | 20 | 1 |
| NoColorChange_Eq5 | INT16 | 6 | 1 |
| ColorChangeCost_Eq5 | REAL | 7 | 1 |
| ColorChangeActionLocal_Eq5 | CLOB | 40 | 1 |
| ColorChangeAction_Eq5 | CLOB | 20 | 1 |
| PrintInkType_Eq6 | CLOB | 20 | 1 |
| PrintInk1Coverage_Eq6 | REAL | 7 | 1 |
| PrintInk2Type_Eq6 | CLOB | 20 | 1 |
| PrintInk2Coverage_Eq6 | REAL | 7 | 1 |
| PrintInk3Type_Eq6 | CLOB | 20 | 1 |
| PrintInk3Coverage_Eq6 | REAL | 7 | 1 |
| PrintInk1NoColors_Eq6 | INT16 | 6 | 1 |
| PrintInk2NoColors_Eq6 | INT16 | 6 | 1 |
| PrintInk3NoColors_Eq6 | INT16 | 6 | 1 |
| NoColors_Eq6 | INT16 | 6 | 1 |
| ColorDescr_Eq6 | CLOB | 80 | 1 |
| Is_LabelSizeInkCov_Press_Eq6 | BOOLEAN | 5 | 1 |
| FloodInkType_Eq6 | CLOB | 20 | 1 |
| FloodInk1Coverage_Eq6 | REAL | 7 | 1 |
| FloodInk2Type_Eq6 | CLOB | 20 | 1 |
| FloodInk2Coverage_Eq6 | REAL | 7 | 1 |
| FloodInk3Type_Eq6 | CLOB | 20 | 1 |
| FloodInk3Coverage_Eq6 | REAL | 7 | 1 |
| FloodInk1NoColors_Eq6 | INT16 | 6 | 1 |
| FloodInk2NoColors_Eq6 | INT16 | 6 | 1 |
| FloodInk3NoColors_Eq6 | INT16 | 6 | 1 |
| NoFloods_Eq6 | INT16 | 6 | 1 |
| NoAround_PrintCylinder_Eq6 | INT32 | 11 | 1 |
| NoPlateChange_Eq6 | INT16 | 6 | 1 |
| PlateChangeCost_Eq6 | REAL | 7 | 1 |
| PlateChangeActionLocal_Eq6 | CLOB | 40 | 1 |
| PlateChangeAction_Eq6 | CLOB | 20 | 1 |
| NoColorChange_Eq6 | INT16 | 6 | 1 |
| ColorChangeCost_Eq6 | REAL | 7 | 1 |
| ColorChangeActionLocal_Eq6 | CLOB | 40 | 1 |
| ColorChangeAction_Eq6 | CLOB | 255 | 1 |
| Tool_NumberAround_Eq2 | INT16 | 6 | 1 |
| Tool_NumberAround_Eq3 | INT16 | 6 | 1 |
| Tool_NumberAround_Eq4 | INT16 | 6 | 1 |
| Tool_NumberAround_Eq5 | INT16 | 6 | 1 |
| Tool_NumberAround_Eq6 | INT16 | 6 | 1 |
| InLinePriming_Rate_Eq2 | REAL | 7 | 1 |
| InLinePriming_Rate_Eq3 | REAL | 7 | 1 |
| InLinePriming_Rate_Eq4 | REAL | 7 | 1 |
| InLinePriming_Rate_Eq5 | REAL | 7 | 1 |
| InLinePriming_Rate_Eq6 | REAL | 7 | 1 |
| InLinePriming_State_Eq2 | INT16 | 6 | 1 |
| InLinePriming_State_Eq3 | INT16 | 6 | 1 |
| InLinePriming_State_Eq4 | INT16 | 6 | 1 |
| InLinePriming_State_Eq5 | INT16 | 6 | 1 |
| InLinePriming_State_Eq6 | INT16 | 6 | 1 |

### Estimate_Activity

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| Estimate_ID | CLOB | 10 | 1 |
| Employee_ID | CLOB | 10 | 1 |
| Employee_Name | CLOB | 60 | 1 |
| Creation_Date | TIMESTAMP | 19 | 1 |
| Creation_Time | INTERVAL | 10 | 1 |
| Contact_ID | CLOB | 10 | 1 |
| Contact_Name | CLOB | 50 | 1 |
| Contact_Phone | CLOB | 20 | 1 |
| Contact_Extension | CLOB | 10 | 1 |
| Call_Back | TIMESTAMP | 19 | 1 |
| Activity | CLOB | 40 | 1 |
| Notes | CLOB | 0 | 1 |
| Email_To_Address | CLOB | 0 | 1 |
| Email_Subject | CLOB | 0 | 1 |
| Email_Message | CLOB | 0 | 1 |
| Email_Sent | BOOLEAN | 5 | 1 |
| PK_UUID | UUID | 0 | 1 |

### FS_CashFlowClasses

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| Name | CLOB | 50 | 1 |
| CF_Type | CLOB | 20 | 1 |
| Statement_Section | CLOB | 20 | 1 |
| CantDelete | BOOLEAN | 5 | 1 |
| AddBackClassID | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |

### FS_FinancialStatements

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| StatementName | CLOB | 40 | 1 |
| StatementDate | TIMESTAMP | 19 | 1 |
| RoundingPrecision | INT32 | 11 | 1 |
| LevelOfDetail | CLOB | 20 | 1 |
| PrintAccountNumbers | BOOLEAN | 5 | 1 |
| Col_1_PrintColumn | BOOLEAN | 5 | 1 |
| Col_1_PrintPercentages | BOOLEAN | 5 | 1 |
| Col_1_Date | TIMESTAMP | 19 | 1 |
| Col_1_MonthsFromStateDate | INT32 | 11 | 1 |
| Col_1_PeriodsToReport | CLOB | 20 | 1 |
| Col_2_PrintColumn | BOOLEAN | 5 | 1 |
| Col_2_PrintPercentages | BOOLEAN | 5 | 1 |
| Col_2_Date | TIMESTAMP | 19 | 1 |
| Col_2_MonthsFromStateDate | INT32 | 11 | 1 |
| Col_2_PeriodsToReport | CLOB | 20 | 1 |
| Col_3_PrintColumn | BOOLEAN | 5 | 1 |
| Col_3_PrintPercentages | BOOLEAN | 5 | 1 |
| Col_3_Date | TIMESTAMP | 19 | 1 |
| Col_3_MonthsFromStateDate | INT32 | 11 | 1 |
| Col_3_PeriodsToReport | CLOB | 20 | 1 |
| Col_4_PrintColumn | BOOLEAN | 5 | 1 |
| Col_4_PrintPercentages | BOOLEAN | 5 | 1 |
| Col_4_Date | TIMESTAMP | 19 | 1 |
| Col_4_MonthsFromStateDate | INT32 | 11 | 1 |
| Col_4_PeriodsToReport | CLOB | 20 | 1 |
| EnteredBy | CLOB | 50 | 1 |
| EnteredDate | TIMESTAMP | 19 | 1 |
| ModifiedBy | CLOB | 50 | 1 |
| ModifiedDate | TIMESTAMP | 19 | 1 |
| ProfitCentersToPrint | CLOB | 3 | 1 |
| StatementType | CLOB | 40 | 1 |
| EnteredTime | INTERVAL | 10 | 1 |
| ModifiedTime | INTERVAL | 10 | 1 |
| Col_1_ColumnType | CLOB | 20 | 1 |
| Col_2_ColumnType | CLOB | 20 | 1 |
| Col_3_ColumnType | CLOB | 20 | 1 |
| Col_4_ColumnType | CLOB | 20 | 1 |
| StatementType_Localized | CLOB | 40 | 1 |
| Col_1_PeriodsToReport_Local | CLOB | 20 | 1 |
| Col_2_PeriodsToReport_Local | CLOB | 20 | 1 |
| Col_3_PeriodsToReport_Local | CLOB | 20 | 1 |
| Col_4_PeriodsToReport_Local | CLOB | 20 | 1 |
| PK_UUID | UUID | 0 | 1 |
| glPrefix | CLOB | 3 | 1 |

### ForeignCurrency

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| AbbrevPlusName | CLOB | 50 | 1 |
| Abbreviation | CLOB | 3 | 1 |
| Name | CLOB | 40 | 1 |
| Thousands_Separator | CLOB | 2 | 1 |
| Decimal_PlaceHolder | CLOB | 2 | 1 |
| Currency_Symbol | CLOB | 5 | 1 |
| Currency_Is_In_Front | BOOLEAN | 5 | 1 |
| Negative_Currency_Format | BOOLEAN | 5 | 1 |
| DefaultExchangeRate | REAL | 7 | 1 |
| EnteredBy | CLOB | 50 | 1 |
| WarningForRateChange | BOOLEAN | 5 | 1 |
| RateChangePercent | REAL | 7 | 1 |
| EnteredDate | TIMESTAMP | 19 | 1 |
| EnteredTime | INTERVAL | 10 | 1 |
| ModifiedBy | CLOB | 50 | 1 |
| ModifiedDate | TIMESTAMP | 19 | 1 |
| ModifiedTime | INTERVAL | 10 | 1 |
| GL_Acct_Name_GainLossCurr | CLOB | 40 | 1 |
| GL_Acct_Num_GainLossCurr | CLOB | 13 | 1 |
| Inactive | BOOLEAN | 5 | 1 |
| SageCurrencyCode | CLOB | 2 | 1 |
| ExchangeRateDecimals | INT32 | 11 | 1 |
| DefaultExchangeRateID | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |

### ForeignCurrency_Rate

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| ForeignCurrency_ID | INT32 | 11 | 1 |
| ExchangeRate | REAL | 7 | 1 |
| FromDate | TIMESTAMP | 19 | 1 |
| FromTime | INTERVAL | 10 | 1 |
| ToDate | TIMESTAMP | 19 | 1 |
| ToTime | INTERVAL | 10 | 1 |
| EnteredBy | CLOB | 255 | 1 |
| EnteredDate | TIMESTAMP | 19 | 1 |
| EnteredTime | INTERVAL | 10 | 1 |
| ModifiedBy | CLOB | 255 | 1 |
| ModifiedDate | TIMESTAMP | 19 | 1 |
| ModifiedTime | INTERVAL | 10 | 1 |
| Rate_Notes | CLOB | 0 | 1 |
| PK_UUID | UUID | 0 | 1 |

### Freight_Chart

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| Max_Weight | INT32 | 11 | 1 |
| Cost | REAL | 7 | 1 |
| UnitWeight_Cost | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |

### GL_Account_Balances

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| AccountNumber | CLOB | 13 | 1 |
| AcctYear_ID | INT32 | 11 | 1 |
| AcctYear_Month | INT32 | 11 | 1 |
| ProfitCenterNum | CLOB | 3 | 1 |
| AccountType_Abbr | CLOB | 2 | 1 |
| OpeningBalance | REAL | 7 | 1 |
| NonCharge_Activity | REAL | 7 | 1 |
| Chargeable_Activity | REAL | 7 | 1 |
| Total_Activity | REAL | 7 | 1 |
| EndingBalance | REAL | 7 | 1 |
| YTD_NonCharge_Activity | REAL | 7 | 1 |
| YTD_Chargeable_Activity | REAL | 7 | 1 |
| MonthEndDate | TIMESTAMP | 19 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### GL_AccountingConstants

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| LastBalanceSheetAcctNum | CLOB | 5 | 1 |
| FirstIncomeStatementAcctNum | CLOB | 5 | 1 |
| StartPostingAR_To_GL | TIMESTAMP | 19 | 1 |
| StartPushingPOsToAP | TIMESTAMP | 19 | 1 |
| StartPostingAP_To_GL | TIMESTAMP | 19 | 1 |
| Plate_AccntNum | CLOB | 13 | 1 |
| Plate_AccntName | CLOB | 40 | 1 |
| Color_AccntNum | CLOB | 13 | 1 |
| Color_AccntName | CLOB | 40 | 1 |
| PO_Art_AccntNum | CLOB | 13 | 1 |
| PO_Art_AccntName | CLOB | 40 | 1 |
| PO_Plate_AccntNum | CLOB | 13 | 1 |
| PO_Plate_AccntName | CLOB | 40 | 1 |
| PO_Tool_AccntNum | CLOB | 13 | 1 |
| PO_Tool_AccntName | CLOB | 40 | 1 |
| PO_Generic_AccntNum | CLOB | 13 | 1 |
| PO_Generic_AccntName | CLOB | 40 | 1 |
| Misc_AccntNum | CLOB | 13 | 1 |
| Misc_AccntName | CLOB | 40 | 1 |
| Freight_AccntNum | CLOB | 13 | 1 |
| Freight_AccntName | CLOB | 40 | 1 |
| TaxAPI_CreditPostTemplate | CLOB | 0 | 1 |
| TaxAPI_CreditReissueTemplate | CLOB | 0 | 1 |
| CreditMemoAmount_AccntNum | CLOB | 13 | 1 |
| CreditMemoAmount_AccntName | CLOB | 40 | 1 |
| InvoiceLine_AccntNum | CLOB | 13 | 1 |
| InvoiceLine_AccntName | CLOB | 40 | 1 |
| SP_InvoiceLine_AccntNum | CLOB | 13 | 1 |
| SP_InvoiceLine_AccntName | CLOB | 40 | 1 |
| SP_Misc_AccntNum | CLOB | 13 | 1 |
| SP_Misc_AccntName | CLOB | 40 | 1 |
| SP_Freight_AccntNum | CLOB | 13 | 1 |
| SP_Freight_AccntName | CLOB | 40 | 1 |
| PTSS_IP_1 | CLOB | 3 | 1 |
| PTSS_IP_2 | CLOB | 3 | 1 |
| PTSS_IP_3 | CLOB | 3 | 1 |
| PTSS_IP_4 | CLOB | 3 | 1 |
| PTSS_IP_Port | CLOB | 6 | 1 |
| PTSS_Password | CLOB | 20 | 1 |
| PK_UUID | UUID | 0 | 1 |
| TaxAPI_Post | CLOB | 0 | 1 |
| TaxAPI_runAPI | BOOLEAN | 5 | 1 |
| TaxAPI_InvoiceReissueTemplate | CLOB | 0 | 1 |
| TaxAPI_TemplateName | CLOB | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |
| TaxAPI_DebitPostTemplate | CLOB | 0 | 1 |
| TaxAPI_DebitReissueTemplate | CLOB | 0 | 1 |
| IntercompanyTransferPriceLevel | REAL | 7 | 1 |

### GL_AccountingYears

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| YearBegins | TIMESTAMP | 19 | 1 |
| YearEnds | TIMESTAMP | 19 | 1 |
| NumberOfMonths | INT32 | 11 | 1 |
| AcctYearLabel | CLOB | 10 | 1 |
| AccountingYearStatus | CLOB | 20 | 1 |
| LastMonthClosed | CLOB | 20 | 1 |
| M_1_Name | CLOB | 20 | 1 |
| M_1_1stDay | TIMESTAMP | 19 | 1 |
| M_1_LastDay | TIMESTAMP | 19 | 1 |
| M_1_Status | CLOB | 20 | 1 |
| M_1_StatusChangedBy | CLOB | 50 | 1 |
| M_1_StatusChangeDate | TIMESTAMP | 19 | 1 |
| M_2_Name | CLOB | 20 | 1 |
| M_2_1stDay | TIMESTAMP | 19 | 1 |
| M_2_LastDay | TIMESTAMP | 19 | 1 |
| M_2_Status | CLOB | 20 | 1 |
| M_2_StatusChangedBy | CLOB | 50 | 1 |
| M_2_StatusChangeDate | TIMESTAMP | 19 | 1 |
| M_3_Name | CLOB | 20 | 1 |
| M_3_1stDay | TIMESTAMP | 19 | 1 |
| M_3_LastDay | TIMESTAMP | 19 | 1 |
| M_3_Status | CLOB | 20 | 1 |
| M_3_StatusChangedBy | CLOB | 50 | 1 |
| M_3_StatusChangeDate | TIMESTAMP | 19 | 1 |
| M_4_Name | CLOB | 20 | 1 |
| M_4_1stDay | TIMESTAMP | 19 | 1 |
| M_4_LastDay | TIMESTAMP | 19 | 1 |
| M_4_Status | CLOB | 20 | 1 |
| M_4_StatusChangedBy | CLOB | 50 | 1 |
| M_4_StatusChangeDate | TIMESTAMP | 19 | 1 |
| M_5_Name | CLOB | 20 | 1 |
| M_5_1stDay | TIMESTAMP | 19 | 1 |
| M_5_LastDay | TIMESTAMP | 19 | 1 |
| M_5_Status | CLOB | 20 | 1 |
| M_5_StatusChangedBy | CLOB | 50 | 1 |
| M_5_StatusChangeDate | TIMESTAMP | 19 | 1 |
| M_6_Name | CLOB | 20 | 1 |
| M_6_1stDay | TIMESTAMP | 19 | 1 |
| M_6_LastDay | TIMESTAMP | 19 | 1 |
| M_6_Status | CLOB | 20 | 1 |
| M_6_StatusChangedBy | CLOB | 50 | 1 |
| M_6_StatusChangeDate | TIMESTAMP | 19 | 1 |
| M_7_Name | CLOB | 20 | 1 |
| M_7_1stDay | TIMESTAMP | 19 | 1 |
| M_7_LastDay | TIMESTAMP | 19 | 1 |
| M_7_Status | CLOB | 20 | 1 |
| M_7_StatusChangedBy | CLOB | 50 | 1 |
| M_7_StatusChangeDate | TIMESTAMP | 19 | 1 |
| M_8_Name | CLOB | 20 | 1 |
| M_8_1stDay | TIMESTAMP | 19 | 1 |
| M_8_LastDay | TIMESTAMP | 19 | 1 |
| M_8_Status | CLOB | 20 | 1 |
| M_8_StatusChangedBy | CLOB | 50 | 1 |
| M_8_StatusChangeDate | TIMESTAMP | 19 | 1 |
| M_9_Name | CLOB | 20 | 1 |
| M_9_1stDay | TIMESTAMP | 19 | 1 |
| M_9_LastDay | TIMESTAMP | 19 | 1 |
| M_9_Status | CLOB | 20 | 1 |
| M_9_StatusChangedBy | CLOB | 50 | 1 |
| M_9_StatusChangeDate | TIMESTAMP | 19 | 1 |
| M10_Name | CLOB | 20 | 1 |
| M10_1stDay | TIMESTAMP | 19 | 1 |
| M10_LastDay | TIMESTAMP | 19 | 1 |
| M10_Status | CLOB | 20 | 1 |
| M10_StatusChangedBy | CLOB | 50 | 1 |
| M10_StatusChangeDate | TIMESTAMP | 19 | 1 |
| M11_Name | CLOB | 20 | 1 |
| M11_1stDay | TIMESTAMP | 19 | 1 |
| M11_LastDay | TIMESTAMP | 19 | 1 |
| M11_Status | CLOB | 20 | 1 |
| M11_StatusChangedBy | CLOB | 50 | 1 |
| M11_StatusChangeDate | TIMESTAMP | 19 | 1 |
| M12_Name | CLOB | 20 | 1 |
| M12_1stDay | TIMESTAMP | 19 | 1 |
| M12_LastDay | TIMESTAMP | 19 | 1 |
| M12_Status | CLOB | 20 | 1 |
| M12_StatusChangedBy | CLOB | 50 | 1 |
| M12_StatusChangeDate | TIMESTAMP | 19 | 1 |
| EnteredBy | CLOB | 50 | 1 |
| EnterDate | TIMESTAMP | 19 | 1 |
| ModifyBy | CLOB | 50 | 1 |
| ModifyDate | TIMESTAMP | 19 | 1 |
| EnteredTime | INTERVAL | 10 | 1 |
| ModifyTime | INTERVAL | 10 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### GL_Analysis_View

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| View_Name | CLOB | 30 | 1 |
| ToDate | TIMESTAMP | 19 | 1 |
| DisplayMode | CLOB | 20 | 1 |
| FromDate | TIMESTAMP | 19 | 1 |
| DateRangeSelected | CLOB | 31 | 1 |
| PK_UUID | UUID | 0 | 1 |
| glPrefix | CLOB | 3 | 1 |

### GL_AssignGLDistribution

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| AccountNumber | CLOB | 13 | 1 |
| AccountName | CLOB | 40 | 1 |
| Percent_Applied | REAL | 7 | 1 |
| CustomProd_UniqueID | CLOB | 10 | 1 |
| StockProd_ID | CLOB | 10 | 1 |
| ID | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |

### GL_Balances_Access

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| UserName | CLOB | 47 | 1 |
| UserActivity | CLOB | 30 | 1 |
| AVL_Field3_NotUsed | CLOB | 0 | 1 |
| PK_UUID | UUID | 0 | 1 |

### GL_Budgets

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| AcctYearLabel | CLOB | 10 | 1 |
| AcctYearID | INT32 | 11 | 1 |
| AcctYearEndDate | TIMESTAMP | 19 | 1 |
| EnteredBy | CLOB | 50 | 1 |
| ModifiedBy | CLOB | 50 | 1 |
| EnteredDate | TIMESTAMP | 19 | 1 |
| ModifyDate | TIMESTAMP | 19 | 1 |
| EnteredTime | INTERVAL | 10 | 1 |
| ModifyTime | INTERVAL | 10 | 1 |
| PK_UUID | UUID | 0 | 1 |

### GL_Budgets_Accounts

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| GL_Budgets_ID | INT32 | 11 | 1 |
| AcctYearLabel | CLOB | 10 | 1 |
| AcctYearID | INT32 | 11 | 1 |
| AcctYearEndDate | TIMESTAMP | 19 | 1 |
| AccountNumber | CLOB | 13 | 1 |
| Month1EndDate | TIMESTAMP | 19 | 1 |
| Month1Amount | INT32 | 11 | 1 |
| Month2EndDate | TIMESTAMP | 19 | 1 |
| Month2Amount | INT32 | 11 | 1 |
| Month3EndDate | TIMESTAMP | 19 | 1 |
| Month3Amount | INT32 | 11 | 1 |
| Month4EndDate | TIMESTAMP | 19 | 1 |
| Month4Amount | INT32 | 11 | 1 |
| Month5EndDate | TIMESTAMP | 19 | 1 |
| Month5Amount | INT32 | 11 | 1 |
| Month6EndDate | TIMESTAMP | 19 | 1 |
| Month6Amount | INT32 | 11 | 1 |
| Month7EndDate | TIMESTAMP | 19 | 1 |
| Month7Amount | INT32 | 11 | 1 |
| Month8EndDate | TIMESTAMP | 19 | 1 |
| Month8Amount | INT32 | 11 | 1 |
| Month9EndDate | TIMESTAMP | 19 | 1 |
| Month9Amount | INT32 | 11 | 1 |
| Month10EndDate | TIMESTAMP | 19 | 1 |
| Month10Amount | INT32 | 11 | 1 |
| Month11EndDate | TIMESTAMP | 19 | 1 |
| Month11Amount | INT32 | 11 | 1 |
| Month12EndDate | TIMESTAMP | 19 | 1 |
| Month12Amount | INT32 | 11 | 1 |
| TotalForYear | INT32 | 11 | 1 |
| AcctYearBeginDate | TIMESTAMP | 19 | 1 |
| PK_UUID | UUID | 0 | 1 |

### GL_COA_FAT

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ChartOfAccounts_ID | INT32 | 11 | 1 |
| AccountUsageGuidelines | CLOB | 0 | 1 |
| InactivationNotes | CLOB | 0 | 1 |
| PK_UUID | UUID | 0 | 1 |

### GL_ChartOfAccounts

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| AccountNumber | CLOB | 13 | 1 |
| BaseAccountNumber | CLOB | 5 | 1 |
| ProfitCenterNumber | CLOB | 3 | 1 |
| AccountName | CLOB | 40 | 1 |
| FinancialStatementClass | CLOB | 40 | 1 |
| SpecialType | CLOB | 40 | 1 |
| Inactive | BOOLEAN | 5 | 1 |
| EnteredBy | CLOB | 50 | 1 |
| EnteredDate | TIMESTAMP | 19 | 1 |
| ModifiedBy | CLOB | 50 | 1 |
| ModifiedDate | TIMESTAMP | 19 | 1 |
| AccountType | CLOB | 20 | 1 |
| CashFlowClass_ID | INT32 | 11 | 1 |
| CashFlowClass_Name | CLOB | 50 | 1 |
| EnteredTime | INTERVAL | 10 | 1 |
| ModifiedTime | INTERVAL | 10 | 1 |
| FinancialStatementClass_Local | CLOB | 80 | 1 |
| AccountType_Local | CLOB | 40 | 1 |
| SpecialType_Local | CLOB | 80 | 1 |
| Group_code | CLOB | 20 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |
| glLocationPrefix | CLOB | 3 | 1 |

### GL_Detail_Activity

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| AccountNumber | CLOB | 13 | 1 |
| SourceDocument_Key | CLOB | 15 | 1 |
| Journal | CLOB | 10 | 1 |
| PostToDate | TIMESTAMP | 19 | 1 |
| SourceDoc_Date | TIMESTAMP | 19 | 1 |
| SourceDoc_ID | INT32 | 11 | 1 |
| Company_Memo | CLOB | 80 | 1 |
| Debit | REAL | 7 | 1 |
| Credit | REAL | 7 | 1 |
| DateClearedBank | TIMESTAMP | 19 | 1 |
| GL_Balances_ID | INT32 | 11 | 1 |
| TicketNumber | CLOB | 12 | 1 |
| AccountType_Abbr | CLOB | 2 | 1 |
| AP_InvoiceNum | CLOB | 20 | 1 |
| AP_PO_Number | CLOB | 10 | 1 |
| PK_UUID | UUID | 0 | 1 |
| FCAmountClearedBank | REAL | 7 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### GL_NetIncome

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| AcctYear_ID | INT32 | 11 | 1 |
| ProfitCenterNum | CLOB | 3 | 1 |
| YearToDate_NetIncome | REAL | 7 | 1 |
| NetIncome_ThisMonth | REAL | 7 | 1 |
| MonthEndDate | TIMESTAMP | 19 | 1 |
| PK_UUID | UUID | 0 | 1 |
| glPrefix | CLOB | 3 | 1 |

### GL_ProfitCenter

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| ProfitCenterNumber | CLOB | 3 | 1 |
| ProfitCenterName | CLOB | 20 | 1 |
| UsageGuidelines | CLOB | 0 | 1 |
| InActive | BOOLEAN | 5 | 1 |
| InactivationNote | CLOB | 0 | 1 |
| EnteredBy | CLOB | 50 | 1 |
| EnteredDate | TIMESTAMP | 19 | 1 |
| ModifiedBy | CLOB | 50 | 1 |
| ModifiedDate | TIMESTAMP | 19 | 1 |
| EnteredTime | INTERVAL | 10 | 1 |
| ModifiedTime | INTERVAL | 10 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |
| mfgLocation | CLOB | 0 | 1 |

### GL_View_Accounts

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| GL_Analysis_View_ID | INT32 | 11 | 1 |
| AccountNumber | CLOB | 13 | 1 |
| AccountName | CLOB | 40 | 1 |
| Delete_View | BOOLEAN | 5 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### HP_PrintOS

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| PK_UUID | UUID | 0 | 0 |
| ID | CLOB | 20 | 1 |
| TicketNum | CLOB | 12 | 1 |
| EntryDate | TIMESTAMP | 19 | 1 |
| PressSerialNum | CLOB | 80 | 1 |
| PressID | CLOB | 40 | 1 |
| Impress1Color | INT32 | 11 | 1 |
| Impress2Color | INT32 | 11 | 1 |
| ImpressNColor | INT32 | 11 | 1 |
| EPM_Impress | INT32 | 11 | 1 |
| ImpressType | CLOB | 40 | 1 |
| impressions | INT32 | 11 | 1 |
| InkUnits | CLOB | 40 | 1 |
| JobCompleteTime | INTERVAL | 10 | 1 |
| JobElapsedTime | INTERVAL | 10 | 1 |
| JobName | CLOB | 255 | 1 |
| JobProgress | CLOB | 40 | 1 |
| JobSubmitTime | INTERVAL | 10 | 1 |
| Marker | REAL | 7 | 1 |
| printedJobID | CLOB | 80 | 1 |
| OneShotImpress | INT32 | 11 | 1 |
| PrintedSheets | INT32 | 11 | 1 |
| RepeatLength | INT32 | 11 | 1 |
| siteName | CLOB | 127 | 1 |
| SubstrateUnits | CLOB | 40 | 1 |
| EntryTime | INTERVAL | 10 | 1 |
| useOfVDP | CLOB | 80 | 1 |
| copies | INT32 | 11 | 1 |
| width | REAL | 7 | 1 |
| height | REAL | 7 | 1 |
| duplex | BOOLEAN | 5 | 1 |
| jobCollation | BOOLEAN | 5 | 1 |
| JobSubmitTimeUTC | CLOB | 40 | 1 |
| JobCompleteTimeUTC | CLOB | 40 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### HP_PrintOS_InkSub

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| PK_UUID | UUID | 0 | 0 |
| NameOfMaterial | CLOB | 0 | 1 |
| AmountUsed | INT32 | 11 | 1 |
| ID | CLOB | 20 | 1 |
| HP_PrintOSID | CLOB | 255 | 1 |
| TypeOfRec | CLOB | 255 | 1 |
| inkSerialNumber | CLOB | 40 | 1 |

### HP_PrintOS_Prefs

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| PK_UUID | UUID | 0 | 0 |
| StartMarker | REAL | 7 | 1 |
| delayTime | INT32 | 11 | 1 |

### HP_PrintOS_storedData

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| pID | UUID | 0 | 0 |
| ID | CLOB | 0 | 1 |
| hpData | CLOB | 0 | 1 |
| currentDate | TIMESTAMP | 19 | 1 |
| currentTime | INTERVAL | 10 | 1 |

### HTTP_Log

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| URL_Request | CLOB | 0 | 1 |
| Header_Request | CLOB | 0 | 1 |
| Web_Client_IP_Address | CLOB | 255 | 1 |
| Server_IP_Address | CLOB | 255 | 1 |
| User_Name | CLOB | 255 | 1 |
| Password | CLOB | 255 | 1 |
| Creation_DateStamp | TIMESTAMP | 19 | 1 |
| Creation_TimeStamp | INTERVAL | 10 | 1 |
| Response | CLOB | 0 | 1 |
| PK_UUID | UUID | 0 | 1 |
| Body | CLOB | 0 | 1 |
| Label_Traxx_Module | CLOB | 255 | 1 |
| Authentication_Required | BOOLEAN | 5 | 1 |
| Authentication_Failed | BOOLEAN | 5 | 1 |
| SSL_Required_module | BOOLEAN | 5 | 1 |
| SSL_Required | BOOLEAN | 5 | 1 |
| SSL_Conection | BOOLEAN | 5 | 1 |
| Header_Response | CLOB | 0 | 1 |
| Return_Status | CLOB | 255 | 1 |
| Duration | INTERVAL | 10 | 1 |
| Reference | CLOB | 255 | 1 |
| Restricted_IP | BOOLEAN | 5 | 1 |
| Module_Status | CLOB | 255 | 1 |
| Error_code | CLOB | 0 | 1 |
| Error_EXE | BOOLEAN | 5 | 1 |
| Client | BOOLEAN | 5 | 1 |
| Decrypt_Method | CLOB | 40 | 1 |
| Decrypt_Password | CLOB | 40 | 1 |
| Field_30 | CLOB | 255 | 1 |

### HoursOff

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| AssociateNum | CLOB | 10 | 1 |
| HrDate | TIMESTAMP | 19 | 1 |
| Hours | REAL | 7 | 1 |
| HrType | CLOB | 10 | 1 |
| HrType_Local | CLOB | 255 | 1 |
| PK_UUID | UUID | 0 | 1 |

### Http_Client_queue

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| PK_UUID | UUID | 0 | 0 |
| Created_date | TIMESTAMP | 19 | 1 |
| Created_time | INTERVAL | 10 | 1 |
| Request | None | 0 | 1 |
| Priority | INT32 | 11 | 1 |
| Send_ok | BOOLEAN | 5 | 1 |
| Response | None | 0 | 1 |
| Modified_date | TIMESTAMP | 19 | 1 |
| Modified_time | INTERVAL | 10 | 1 |
| Reference | CLOB | 255 | 1 |
| Request_content | BLOB | 0 | 1 |
| Responce_content | BLOB | 0 | 1 |

### InOutStatus

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| Associate_Number | CLOB | 10 | 1 |
| Status | CLOB | 31 | 1 |
| BackAt | CLOB | 31 | 1 |
| Note | CLOB | 80 | 1 |
| ModifiedDate | TIMESTAMP | 19 | 1 |
| ModifiedTime | INTERVAL | 10 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### InkInventory

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| Color | CLOB | 35 | 1 |
| Description | CLOB | 40 | 1 |
| Series | CLOB | 25 | 1 |
| FormulaNo | CLOB | 20 | 1 |
| Weight | REAL | 7 | 1 |
| PricePerPound | REAL | 7 | 1 |
| InkCost | REAL | 7 | 1 |
| Notes | CLOB | 0 | 1 |
| PK_UUID | UUID | 0 | 1 |

### Inspection

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 0 | 1 |
| IP_Address | CLOB | 0 | 1 |
| PortNo | CLOB | 0 | 1 |
| PressID | CLOB | 0 | 1 |
| AVT_Name | CLOB | 0 | 1 |
| NetworkDrive | CLOB | 0 | 1 |
| PK_UUID | UUID | 0 | 1 |
| Use_NoAround | BOOLEAN | 5 | 1 |

### IntercompanyTransferTemplate

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| PK_UUID | UUID | 0 | 1 |
| Type | CLOB | 255 | 1 |
| OriginPrefix | CLOB | 3 | 1 |
| OriginName | CLOB | 255 | 1 |
| OriginDebit | CLOB | 255 | 1 |
| OriginDebitName | CLOB | 255 | 1 |
| OriginCredit | CLOB | 255 | 1 |
| OriginCreditName | CLOB | 255 | 1 |
| ReceivePrefix | CLOB | 35 | 1 |
| ReceiveName | CLOB | 255 | 1 |
| ReceiveDebitName | CLOB | 255 | 1 |
| ReceiveCredit | CLOB | 255 | 1 |
| ReceiveCreditName | CLOB | 255 | 1 |
| ID | CLOB | 10 | 1 |
| ReceiveDebit | CLOB | 255 | 1 |

### Invent_Adj_Log

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| Inventory_ID | CLOB | 10 | 1 |
| Adj_TimeStamp | INT32 | 11 | 1 |
| Adj_Date | TIMESTAMP | 19 | 1 |
| Adj_Time | INTERVAL | 10 | 1 |
| Emp_ID | CLOB | 10 | 1 |
| Emp_FName | CLOB | 20 | 1 |
| Emp_LName | CLOB | 20 | 1 |
| Adj_Quantity | REAL | 7 | 1 |
| Adj_Notes | CLOB | 80 | 1 |
| PK_UUID | UUID | 0 | 1 |

### Inventory

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| VendorID | CLOB | 10 | 1 |
| BasisWt | REAL | 7 | 1 |
| Caliper | REAL | 7 | 1 |
| Color | CLOB | 40 | 1 |
| S_Type | CLOB | 20 | 1 |
| Coated2Side | BOOLEAN | 5 | 1 |
| Coated | BOOLEAN | 5 | 1 |
| Description | CLOB | 80 | 1 |
| SizeAcrossGrain | REAL | 7 | 1 |
| SizeWithGrain | REAL | 7 | 1 |
| SizeCalc | CLOB | 20 | 1 |
| MWeight | REAL | 7 | 1 |
| PricePerM | REAL | 7 | 1 |
| Quantity | REAL | 7 | 1 |
| Notes | CLOB | 0 | 1 |
| Price_Method | CLOB | 30 | 1 |
| Part_Type | CLOB | 30 | 1 |
| Part_Number | CLOB | 40 | 1 |
| Allocated | REAL | 7 | 1 |
| Available | REAL | 7 | 1 |
| BackOrder | REAL | 7 | 1 |
| Minimum | REAL | 7 | 1 |
| Maximum | REAL | 7 | 1 |
| Unit | CLOB | 20 | 1 |
| VendorPartNo | CLOB | 40 | 1 |
| Location | CLOB | 40 | 1 |
| Inactive | BOOLEAN | 5 | 1 |
| EnteredBy | CLOB | 50 | 1 |
| ModifiedBy | CLOB | 50 | 1 |
| EnteredDate | TIMESTAMP | 19 | 1 |
| ModifiedDate | TIMESTAMP | 19 | 1 |
| EnteredTime | INTERVAL | 10 | 1 |
| ModifiedTime | INTERVAL | 10 | 1 |
| BOM_ShowDecimal | BOOLEAN | 5 | 1 |
| BOM_DecimalsToShow | INT32 | 11 | 1 |
| Unit_Local | CLOB | 20 | 1 |
| PK_UUID | UUID | 0 | 1 |
| Currency_ID | INT32 | 11 | 1 |
| Currency_ExchangeRate | REAL | 7 | 1 |
| FC_PricePerM | REAL | 7 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |
| Tag | CLOB | 3 | 1 |
| invStatus | CLOB | 0 | 1 |
| invStatus_Org | CLOB | 255 | 1 |

### InventoryLog

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| StockProdID | CLOB | 10 | 1 |
| iTimeStamp | INT32 | 11 | 1 |
| I_Date | TIMESTAMP | 19 | 1 |
| I_Time | INTERVAL | 10 | 1 |
| Name | CLOB | 30 | 1 |
| Qty | INT32 | 11 | 1 |
| Ticket_ID | CLOB | 10 | 1 |
| Notes | CLOB | 80 | 1 |
| Kit_Product_ID | CLOB | 10 | 1 |
| Kit_Part_Number | CLOB | 40 | 1 |
| PackSlipItem_ID | CLOB | 10 | 1 |
| PK_UUID | UUID | 0 | 1 |

### Inventory_Item

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| Inventory_ID | CLOB | 10 | 1 |
| PO_ItemID | CLOB | 10 | 1 |
| Rec_TimeStamp | INT32 | 11 | 1 |
| Date_Received | TIMESTAMP | 19 | 1 |
| Time_Received | INTERVAL | 10 | 1 |
| Quantity | REAL | 7 | 1 |
| Returned_Qty | REAL | 7 | 1 |
| Unit | CLOB | 20 | 1 |
| Unit_Cost | REAL | 7 | 1 |
| u1 | CLOB | 0 | 1 |
| u2 | CLOB | 0 | 1 |
| StockProduct_ID | CLOB | 10 | 1 |
| Notes | CLOB | 0 | 1 |
| EntryDate | TIMESTAMP | 19 | 1 |
| EntryBy | CLOB | 50 | 1 |
| ModifyDate | TIMESTAMP | 19 | 1 |
| ModifyBy | CLOB | 50 | 1 |
| A4LinkDate | TIMESTAMP | 19 | 1 |
| SendToA4 | CLOB | 20 | 1 |
| A4VoucherID | INT32 | 11 | 1 |
| A4VendorID | INT32 | 11 | 1 |
| A4LinkBatchID | INT32 | 11 | 1 |
| ReceiptBatchID | INT32 | 11 | 1 |
| ReceiptBatchStatus | CLOB | 20 | 1 |
| PushPORecToAP_Status | CLOB | 20 | 1 |
| AP_Invoice_ID | INT32 | 11 | 1 |
| EntryTime | INTERVAL | 10 | 1 |
| ModifyTime | INTERVAL | 10 | 1 |
| PK_UUID | UUID | 0 | 1 |
| FC_Unit_Cost | REAL | 7 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### Inventory_Level

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| Inventory_ID | CLOB | 10 | 1 |
| Quantity | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |

### Invoice

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| Number | CLOB | 10 | 1 |
| TicketNum | CLOB | 12 | 1 |
| CustomerName | CLOB | 80 | 1 |
| CustomerNumber | CLOB | 10 | 1 |
| Terms | CLOB | 45 | 1 |
| TaxRate | REAL | 7 | 1 |
| STotal | REAL | 7 | 1 |
| Tax | REAL | 7 | 1 |
| Freight | REAL | 7 | 1 |
| MiscText | CLOB | 80 | 1 |
| Misc | REAL | 7 | 1 |
| Total | REAL | 7 | 1 |
| Notes | CLOB | 0 | 1 |
| SalesCommissionPercent | REAL | 7 | 1 |
| County | CLOB | 20 | 1 |
| TotalPaid | REAL | 7 | 1 |
| iDate | TIMESTAMP | 19 | 1 |
| iType | CLOB | 10 | 1 |
| PurchItems | REAL | 7 | 1 |
| Balance | REAL | 7 | 1 |
| Taxed | BOOLEAN | 5 | 1 |
| Discount | REAL | 7 | 1 |
| Closed | BOOLEAN | 5 | 1 |
| PlateCharge | REAL | 7 | 1 |
| ColorCharge | REAL | 7 | 1 |
| RInvoice | CLOB | 10 | 1 |
| SalesRepNo | CLOB | 10 | 1 |
| ZipCode | CLOB | 15 | 1 |
| Territory | CLOB | 2 | 1 |
| Area | CLOB | 2 | 1 |
| PO_Art | REAL | 7 | 1 |
| PO_Plate | REAL | 7 | 1 |
| PO_Tool | REAL | 7 | 1 |
| PO_Generic | REAL | 7 | 1 |
| MFGRepCommPercent | REAL | 7 | 1 |
| MFG_ID | CLOB | 10 | 1 |
| MFG_Name | CLOB | 80 | 1 |
| IsLocked | CLOB | 10 | 1 |
| Tax_STotal | BOOLEAN | 5 | 1 |
| Tax_Plate | BOOLEAN | 5 | 1 |
| Tax_Color | BOOLEAN | 5 | 1 |
| Tax_PO | BOOLEAN | 5 | 1 |
| Tax_Misc | BOOLEAN | 5 | 1 |
| Tax_Freight | BOOLEAN | 5 | 1 |
| StockProdDiscnt | REAL | 7 | 1 |
| STotalDiscount | REAL | 7 | 1 |
| TaxRate2 | REAL | 7 | 1 |
| Tax2 | REAL | 7 | 1 |
| State_Province | CLOB | 25 | 1 |
| TaxCredit | REAL | 7 | 1 |
| A4_UniqueID | INT32 | 11 | 1 |
| EntryDate | TIMESTAMP | 19 | 1 |
| EntryBy | CLOB | 50 | 1 |
| ModifyDate | TIMESTAMP | 19 | 1 |
| ModifyBy | CLOB | 50 | 1 |
| A4LinkDate | TIMESTAMP | 19 | 1 |
| SendToA4 | CLOB | 20 | 1 |
| A4LinkBatchID | INT32 | 11 | 1 |
| A4DueDate | TIMESTAMP | 19 | 1 |
| A4ClientID | INT32 | 11 | 1 |
| EDIExportDate | TIMESTAMP | 19 | 1 |
| AR_Transaction_ID | INT32 | 11 | 1 |
| PrePay_AR_Bal_ID | INT32 | 11 | 1 |
| PrePay_AR_Trans_ID | INT32 | 11 | 1 |
| PrePay_ARMaint_ID | INT32 | 11 | 1 |
| AR_PostingStatus | CLOB | 30 | 1 |
| Distributed_Amount | REAL | 7 | 1 |
| Undistributed_Amount | REAL | 7 | 1 |
| GL_PostingStatus | CLOB | 10 | 1 |
| GL_Detail_ID | INT32 | 11 | 1 |
| SalesCommissionAmount | REAL | 7 | 1 |
| BilledOnMasterInvoiceNum | CLOB | 10 | 1 |
| MasterInvoicePO_Num | CLOB | 80 | 1 |
| TaxCertificatePrintText | CLOB | 40 | 1 |
| TaxCB_Plate_i | INT32 | 11 | 1 |
| TaxCB_Color_i | INT32 | 11 | 1 |
| TaxCB_AllPOs_i | INT32 | 11 | 1 |
| TaxCB_Misc_i | INT32 | 11 | 1 |
| TaxCB_Freight_i | INT32 | 11 | 1 |
| TaxCB_Discount_i | INT32 | 11 | 1 |
| Tax_TotalSaleAmount | REAL | 7 | 1 |
| Tax_ExemptSaleAmount | REAL | 7 | 1 |
| Tax_ResaleAmount | REAL | 7 | 1 |
| Tax_NonTaxableSalesAmount | REAL | 7 | 1 |
| Tax_TotalAmountSubjectToTax | REAL | 7 | 1 |
| Tax_SalesTaxAmount | REAL | 7 | 1 |
| TaxCB_STotal_i | INT32 | 11 | 1 |
| TaxAmount_Total | REAL | 7 | 1 |
| InvTax_UsesNewTaxSystem | BOOLEAN | 5 | 1 |
| InvTax_ConvertToNewSys | BOOLEAN | 5 | 1 |
| RST_ReversingInvoiceType | CLOB | 10 | 1 |
| RST_SourceInvoiceNum | CLOB | 10 | 1 |
| RST_ReversingInvoiceNum | CLOB | 10 | 1 |
| RST_DuplicateInvoiceNum | CLOB | 10 | 1 |
| EntryTime | INTERVAL | 10 | 1 |
| ModifyTime | INTERVAL | 10 | 1 |
| Currency_ExchangeRate | REAL | 7 | 1 |
| Currency_ID | INT32 | 11 | 1 |
| FCT_TotalPaid | REAL | 7 | 1 |
| FCT_Balance | REAL | 7 | 1 |
| FCT_Total | REAL | 7 | 1 |
| MFGRepCommAmount | REAL | 7 | 1 |
| Enduser_ID | CLOB | 10 | 1 |
| Mex_UUID | CLOB | 40 | 1 |
| Currency_Rate_ID | INT32 | 11 | 1 |
| FC_STotal | REAL | 7 | 1 |
| FC_STotalDiscount | REAL | 7 | 1 |
| FC_TaxAmount_Total | REAL | 7 | 1 |
| FC_PlateCharge | REAL | 7 | 1 |
| FC_ColorCharge | REAL | 7 | 1 |
| FC_PurchItems | REAL | 7 | 1 |
| FC_Misc | REAL | 7 | 1 |
| FC_Freight | REAL | 7 | 1 |
| FC_PO_Art | REAL | 7 | 1 |
| FC_PO_Plate | REAL | 7 | 1 |
| FC_PO_Tool | REAL | 7 | 1 |
| FC_PO_Generic | REAL | 7 | 1 |
| Method_of_Payment | CLOB | 40 | 1 |
| MiscChargeDesc1 | CLOB | 0 | 1 |
| MiscChargeDesc2 | CLOB | 0 | 1 |
| MiscChargeDesc3 | CLOB | 0 | 1 |
| MiscChargeDesc4 | CLOB | 0 | 1 |
| MiscCharge1 | REAL | 7 | 1 |
| MiscCharge2 | REAL | 7 | 1 |
| MiscCharge3 | REAL | 7 | 1 |
| MiscCharge4 | REAL | 7 | 1 |
| FC_MiscCharge1 | REAL | 7 | 1 |
| FC_MiscCharge2 | REAL | 7 | 1 |
| FC_MiscCharge3 | REAL | 7 | 1 |
| FC_MiscCharge4 | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |
| Tag | CLOB | 3 | 1 |
| Manufacture_Tag | CLOB | 3 | 1 |

### InvoiceItem

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| InvoiceNumber | CLOB | 10 | 1 |
| ProductNumber | CLOB | 30 | 1 |
| TicketItemID | CLOB | 10 | 1 |
| OrderQuantity | INT32 | 11 | 1 |
| ShipQuantity | INT32 | 11 | 1 |
| BackOrdered | INT32 | 11 | 1 |
| PricePerM | REAL | 7 | 1 |
| ItemTotal | REAL | 7 | 1 |
| ProdDescr | CLOB | 80 | 1 |
| ShipDate | TIMESTAMP | 19 | 1 |
| PriceMode | CLOB | 20 | 1 |
| ProdDesc2 | CLOB | 80 | 1 |
| Distributed_Amount | REAL | 7 | 1 |
| Undistributed_Amount | REAL | 7 | 1 |
| TaxCB_Item_i | INT32 | 11 | 1 |
| PackSlipItem_ID | CLOB | 10 | 1 |
| PO_Number | CLOB | 30 | 1 |
| MI_Source_ItemID | CLOB | 10 | 1 |
| MI_Source_InvoiceNum | CLOB | 10 | 1 |
| FC_PricePerM | REAL | 7 | 1 |
| FC_ItemTotal | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |
| PriceMode_Local | CLOB | 20 | 1 |
| Order_Weight | REAL | 7 | 1 |
| Ship_Weight | REAL | 7 | 1 |
| Unit_Weight | REAL | 7 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### Invoice_GL_Distribution

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| Invoice_ID | CLOB | 10 | 1 |
| Line_Item_ID | CLOB | 10 | 1 |
| Line_Type | CLOB | 30 | 1 |
| Item_Product_Number | CLOB | 30 | 1 |
| Item_Product_Desc | CLOB | 80 | 1 |
| Account_Number | CLOB | 13 | 1 |
| Account_Name | CLOB | 40 | 1 |
| Distribution_Amount | REAL | 7 | 1 |
| StockProduct_Group | CLOB | 20 | 1 |
| StockProduct_Type | CLOB | 20 | 1 |
| CustomProduct_Group | CLOB | 40 | 1 |
| GL_Detail_ID | INT32 | 11 | 1 |
| AccountTypeAbbr | CLOB | 2 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### Invoice_Tax_Detail

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| InvoiceNumber | CLOB | 10 | 1 |
| Inv_Tax_PackSlip_ID | INT32 | 11 | 1 |
| PackSlipNumber | CLOB | 10 | 1 |
| TicketNumber | CLOB | 12 | 1 |
| SalesTaxRegion_ID | INT32 | 11 | 1 |
| SalesTaxRegionName | CLOB | 80 | 1 |
| SalesTaxRegionRate | REAL | 7 | 1 |
| InvoiceItem_ID | CLOB | 10 | 1 |
| TaxType_ID | INT32 | 11 | 1 |
| TaxTypeRate | REAL | 7 | 1 |
| TaxTypeName | CLOB | 80 | 1 |
| TaxTypeInvoiceDescr | CLOB | 50 | 1 |
| TaxTypeState | CLOB | 25 | 1 |
| TaxTypeCountry | CLOB | 25 | 1 |
| TotalSaleAmount | REAL | 7 | 1 |
| ItemSortKey | CLOB | 30 | 1 |
| ExemptSaleAmount | REAL | 7 | 1 |
| NonTaxableSaleAmount | REAL | 7 | 1 |
| ThisItemIsTaxable | BOOLEAN | 5 | 1 |
| TaxFreight | BOOLEAN | 5 | 1 |
| TaxPlateChange | BOOLEAN | 5 | 1 |
| TaxColorChange | BOOLEAN | 5 | 1 |
| TaxRegionState | CLOB | 25 | 1 |
| TaxRegionCountry | CLOB | 25 | 1 |
| SalesTaxAmount | REAL | 7 | 1 |
| ResaleAmount | REAL | 7 | 1 |
| AVL_x28 | CLOB | 0 | 1 |
| InvoiceDate | TIMESTAMP | 19 | 1 |
| TotalAmountSubjectToTax | REAL | 7 | 1 |
| TaxDetailType | CLOB | 80 | 1 |
| PackSlipCity | CLOB | 40 | 1 |
| PackSlipState | CLOB | 25 | 1 |
| TaxDetailDescription | CLOB | 80 | 1 |
| PackSlipCountry | CLOB | 25 | 1 |
| PackSlipStateSORT | CLOB | 25 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### Invoice_Tax_PackSlip

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| InvoiceNumber | CLOB | 10 | 1 |
| PackSlipNumber | CLOB | 10 | 1 |
| TicketNumber | CLOB | 12 | 1 |
| SalesTaxRegion_ID | INT32 | 11 | 1 |
| ShipAddress_ID | CLOB | 10 | 1 |
| InvoiceDate | TIMESTAMP | 19 | 1 |
| PackSlipCity | CLOB | 40 | 1 |
| PackSlipState | CLOB | 25 | 1 |
| PrintEachType | BOOLEAN | 5 | 1 |
| SalesTaxRegion_Name | CLOB | 80 | 1 |
| AVL_x12 | CLOB | 0 | 1 |
| SalesTaxRegionRate | REAL | 7 | 1 |
| PackSlipCountry | CLOB | 25 | 1 |
| TaxExempt | BOOLEAN | 5 | 1 |
| ResaleCert | BOOLEAN | 5 | 1 |
| Certificate | CLOB | 40 | 1 |
| PrintCertOnInvoice | BOOLEAN | 5 | 1 |
| TotalSaleAmount | REAL | 7 | 1 |
| ExemptSaleAmount | REAL | 7 | 1 |
| ResaleAmount | REAL | 7 | 1 |
| NonTaxableSaleAmount | REAL | 7 | 1 |
| TotalAmountSubjectToTax | REAL | 7 | 1 |
| SalesTaxAmount | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### JDF_AE10_ColorStrategy

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| List_GroupName | CLOB | 40 | 1 |
| Color_Strategy | CLOB | 40 | 1 |
| Ink_Set | CLOB | 10 | 1 |
| PK_UUID | UUID | 0 | 1 |
| Mfg_locations | None | 0 | 1 |

### JDF_Constants

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| BackStage_IP_Address | CLOB | 30 | 1 |
| BackStage_PortNumber | CLOB | 30 | 1 |
| BackStage_DefaultPath | CLOB | 0 | 1 |
| BackStage_URL | CLOB | 0 | 1 |
| LblTrx_IP_Address | CLOB | 30 | 1 |
| LblTrx_PortNumber | CLOB | 30 | 1 |
| LblTrx_DefaultPath | CLOB | 0 | 1 |
| LblTrx_URL | CLOB | 0 | 1 |
| BackStage_Is_JobContainer_Set | BOOLEAN | 5 | 1 |
| BackStage_JobContainerFoldPath | CLOB | 0 | 1 |
| Is_XknAutoTonerUsage | BOOLEAN | 5 | 1 |
| LblTrx_ArtWorkFolder | CLOB | 80 | 1 |
| BackStageJobsAndProductsFolder | CLOB | 80 | 1 |
| BackStage_ProductsFolder | CLOB | 80 | 1 |
| BackStage_ColorStrategyDefault | CLOB | 40 | 1 |
| Log_JDF_Request_Response | BOOLEAN | 5 | 1 |
| CopyPosition_1_5 | REAL | 7 | 1 |
| CopyPosition_2_6 | REAL | 7 | 1 |
| CopyPosition_3_7 | REAL | 7 | 1 |
| CopyPosition_4_8 | REAL | 7 | 1 |
| BackStage_DefaultReportForm | CLOB | 40 | 1 |
| JobNameSeparator | CLOB | 20 | 1 |
| BS_TaskStepRepeatPrint_FilePth | CLOB | 0 | 1 |
| CustomerFolder_Type | INT32 | 11 | 1 |
| MachineName_Artwork | CLOB | 40 | 1 |
| Is_Throttle_On | BOOLEAN | 5 | 1 |
| Delay_between_Jobs | INT32 | 11 | 1 |
| JMF_Device_ID | CLOB | 255 | 1 |
| Use_Http_Helper | BOOLEAN | 5 | 1 |
| Is_Auto_Resource_Subscription | BOOLEAN | 5 | 1 |
| DFE_Type_Code | INT32 | 11 | 1 |
| Send_Ticket_OnSave | BOOLEAN | 5 | 1 |
| Is_Scan_for_AutoSend_JDF | BOOLEAN | 5 | 1 |
| Frames_Lead_In | INT32 | 11 | 1 |
| Frames_Lead_Out | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |
| FilePlan_API_Templates_ID | CLOB | 255 | 1 |
| Is_AE_auto_obsolete_on | BOOLEAN | 5 | 1 |
| AE_Obsolete_TicketName | CLOB | 255 | 1 |
| AEQS_IsProdUp | BOOLEAN | 5 | 1 |
| isFilePlanOrderReversed | BOOLEAN | 5 | 1 |
| Mfg_locations | None | 0 | 1 |
| useExternal_IP | BOOLEAN | 5 | 1 |
| LblTrx_External_IP | CLOB | 30 | 1 |

### JE_JournalEntry

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| PostToDate | TIMESTAMP | 19 | 1 |
| AutoReverse | BOOLEAN | 5 | 1 |
| AutoReverseDate | TIMESTAMP | 19 | 1 |
| JournalEntryMemo | CLOB | 0 | 1 |
| TotalDebits | REAL | 7 | 1 |
| TotalCredits | REAL | 7 | 1 |
| EnteredBy | CLOB | 50 | 1 |
| EnteredDate | TIMESTAMP | 19 | 1 |
| ModifiedBy | CLOB | 50 | 1 |
| ModifedDate | TIMESTAMP | 19 | 1 |
| JournalEntryType | CLOB | 20 | 1 |
| AutoRevJE_ID | INT32 | 11 | 1 |
| SourceOfAutoRevJE_ID | INT32 | 11 | 1 |
| GL_PostStatus | CLOB | 10 | 1 |
| EnteredTime | INTERVAL | 10 | 1 |
| ModifiedTime | INTERVAL | 10 | 1 |
| PK_UUID | UUID | 0 | 1 |
| AutoCreation_RelatedNum | CLOB | 20 | 1 |
| AutoCreation_Type | CLOB | 255 | 1 |

### JE_JournalEntryLine

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| JE_JournalEntry_ID | INT32 | 11 | 1 |
| AccountNumber | CLOB | 13 | 1 |
| AccountName | CLOB | 40 | 1 |
| Debit | REAL | 7 | 1 |
| Credit | REAL | 7 | 1 |
| LineMemo | CLOB | 60 | 1 |
| TicketNumber | CLOB | 12 | 1 |
| AVL_Field9_NotUsed | CLOB | 0 | 1 |
| AccountType_Abbr | CLOB | 2 | 1 |
| GL_Detail_ID | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |

### Keys

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| Two | CLOB | 20 | 1 |
| TwoKey | CLOB | 20 | 1 |
| Three | CLOB | 20 | 1 |
| ThreeKey | CLOB | 20 | 1 |
| Four | CLOB | 20 | 1 |
| FourKey | CLOB | 20 | 1 |
| Company | CLOB | 40 | 1 |
| LastDate | TIMESTAMP | 19 | 1 |
| DemoDate | TIMESTAMP | 19 | 1 |
| LastTime | INTERVAL | 10 | 1 |
| Five | CLOB | 20 | 1 |
| FiveKey | CLOB | 20 | 1 |
| ExpDate | INT16 | 6 | 1 |
| Six | CLOB | 20 | 1 |
| SixKey | CLOB | 20 | 1 |
| Seven | CLOB | 20 | 1 |
| SevenKey | CLOB | 20 | 1 |
| numTagLocations | INT32 | 11 | 1 |
| Eight | CLOB | 20 | 1 |
| EightKey | CLOB | 20 | 1 |
| Nine | CLOB | 20 | 1 |
| NineKey | CLOB | 20 | 1 |
| Ten | CLOB | 20 | 1 |
| TenKey | CLOB | 20 | 1 |
| Eleven | CLOB | 20 | 1 |
| ElevenKey | CLOB | 20 | 1 |
| Twelve | CLOB | 20 | 1 |
| TwelveKey | CLOB | 20 | 1 |
| SerialNumber | CLOB | 20 | 1 |
| ExpansionCode | CLOB | 40 | 1 |
| Fourteen | CLOB | 20 | 1 |
| UsesMetricSystem | BOOLEAN | 5 | 1 |
| MetricSetDate | TIMESTAMP | 19 | 1 |
| Fifteen | CLOB | 20 | 1 |
| Sixteen | CLOB | 20 | 1 |
| Seventeen | CLOB | 20 | 1 |
| AutoTraxx_Expansion | CLOB | 40 | 1 |
| Eighteen | CLOB | 25 | 1 |
| PK_UUID | UUID | 0 | 1 |
| Nineteen | CLOB | 20 | 1 |
| Twenty | CLOB | 25 | 1 |
| TwentyOne | CLOB | 20 | 1 |
| TwentyTwo | CLOB | 20 | 1 |
| TwentyThree | CLOB | 20 | 1 |
| TwentyFour | CLOB | 20 | 1 |

### Keys_Subscription

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| PK_UUID | UUID | 0 | 0 |
| Expires | TIMESTAMP | 19 | 1 |
| Last_login_date | TIMESTAMP | 19 | 1 |
| contractTermExpiration | TIMESTAMP | 19 | 1 |
| nextPaymentPeriod | TIMESTAMP | 19 | 1 |

### Kit_Recipe

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| Kit_Product_ID | CLOB | 10 | 1 |
| Kit_Part_Number | CLOB | 40 | 1 |
| Recipe_Product_ID | CLOB | 10 | 1 |
| Recipe_Part_Number | CLOB | 40 | 1 |
| Recipe_Quantity | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### Knowledge

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| Title | CLOB | 45 | 1 |
| KeyWords | CLOB | 50 | 1 |
| Contents | CLOB | 0 | 1 |
| KDate | TIMESTAMP | 19 | 1 |
| Author | CLOB | 35 | 1 |
| Keyword_subtable | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### LWFile

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| Number | CLOB | 10 | 1 |
| RefNum | CLOB | 30 | 1 |
| RCR1 | BOOLEAN | 5 | 1 |
| Knife1 | BOOLEAN | 5 | 1 |
| CIR1 | BOOLEAN | 5 | 1 |
| Oval1 | BOOLEAN | 5 | 1 |
| Spec1 | BOOLEAN | 5 | 1 |
| ID1 | BOOLEAN | 5 | 1 |
| Roll1 | BOOLEAN | 5 | 1 |
| FanFold1 | BOOLEAN | 5 | 1 |
| Stack1 | BOOLEAN | 5 | 1 |
| Die1 | CLOB | 20 | 1 |
| MSTR | BOOLEAN | 5 | 1 |
| PlacesA2 | CLOB | 20 | 1 |
| PlacesB2 | CLOB | 20 | 1 |
| PlacesC2 | CLOB | 20 | 1 |
| PlacesD2 | CLOB | 20 | 1 |
| PlacesE2 | CLOB | 20 | 1 |
| LocationA2 | CLOB | 60 | 1 |
| LocationB2 | CLOB | 60 | 1 |
| LocationC2 | CLOB | 60 | 1 |
| LoactionD2 | CLOB | 60 | 1 |
| LocationE2 | CLOB | 60 | 1 |
| Buyouts | BOOLEAN | 5 | 1 |
| Stock | BOOLEAN | 5 | 1 |
| Cores | BOOLEAN | 5 | 1 |
| Ink | BOOLEAN | 5 | 1 |
| Cartons | BOOLEAN | 5 | 1 |
| LayerA2 | CLOB | 20 | 1 |
| LayerB2 | CLOB | 20 | 1 |
| LayerC2 | CLOB | 20 | 1 |
| LayerD2 | CLOB | 20 | 1 |
| LayerE2 | CLOB | 20 | 1 |
| SurfAppTo | CLOB | 60 | 1 |
| Substrate | CLOB | 20 | 1 |
| Exposure | CLOB | 20 | 1 |
| AppTemp | CLOB | 20 | 1 |
| ServTemp | CLOB | 20 | 1 |
| AutoApp | BOOLEAN | 5 | 1 |
| PrintType | CLOB | 20 | 1 |
| DistLengthA4 | CLOB | 20 | 1 |
| DistLengthB4 | CLOB | 20 | 1 |
| DistLengthC4 | CLOB | 20 | 1 |
| DistLengthD4 | CLOB | 20 | 1 |
| DistLengthE4 | CLOB | 20 | 1 |
| PRSA4 | BOOLEAN | 5 | 1 |
| PRSB4 | BOOLEAN | 5 | 1 |
| PRSC4 | BOOLEAN | 5 | 1 |
| PRSD4 | BOOLEAN | 5 | 1 |
| PRSE4 | BOOLEAN | 5 | 1 |
| UseLayerA4 | CLOB | 80 | 1 |
| UseLayerB4 | CLOB | 80 | 1 |
| UseLayerC4 | CLOB | 80 | 1 |
| UseLayerD4 | CLOB | 80 | 1 |
| UseLayerE4 | CLOB | 80 | 1 |
| LayerA4 | CLOB | 20 | 1 |
| LayerB4 | CLOB | 20 | 1 |
| LayerC4 | CLOB | 20 | 1 |
| LayerD4 | CLOB | 20 | 1 |
| LayerE4 | CLOB | 20 | 1 |
| PrintsA5 | BOOLEAN | 5 | 1 |
| PrintsB5 | BOOLEAN | 5 | 1 |
| PrintsC5 | BOOLEAN | 5 | 1 |
| ColorsA5 | CLOB | 20 | 1 |
| ColorsB5 | CLOB | 20 | 1 |
| ColorsC5 | CLOB | 20 | 1 |
| TestedA5 | BOOLEAN | 5 | 1 |
| TestedB5 | BOOLEAN | 5 | 1 |
| TestedC5 | BOOLEAN | 5 | 1 |
| SubOKA5 | BOOLEAN | 5 | 1 |
| SubOKB5 | BOOLEAN | 5 | 1 |
| SubOKC5 | BOOLEAN | 5 | 1 |
| SubNumA5 | CLOB | 20 | 1 |
| SubNumB5 | CLOB | 20 | 1 |
| SubNumC5 | CLOB | 20 | 1 |
| AppdByA5 | CLOB | 60 | 1 |
| AppdByB5 | CLOB | 60 | 1 |
| AppdByC5 | CLOB | 60 | 1 |
| PMSA6 | CLOB | 20 | 1 |
| PMSB6 | CLOB | 20 | 1 |
| PMSC6 | CLOB | 20 | 1 |
| PMSD6 | CLOB | 20 | 1 |
| PMSE6 | CLOB | 20 | 1 |
| PMSF6 | CLOB | 20 | 1 |
| PMSG6 | CLOB | 20 | 1 |
| PMSH6 | CLOB | 20 | 1 |
| ColorA6 | CLOB | 20 | 1 |
| ColorB6 | CLOB | 20 | 1 |
| ColorC6 | CLOB | 20 | 1 |
| ColorD6 | CLOB | 20 | 1 |
| ColorE6 | CLOB | 20 | 1 |
| ColorF6 | CLOB | 20 | 1 |
| ColorG6 | CLOB | 20 | 1 |
| ColorH6 | CLOB | 20 | 1 |
| FadeA6 | BOOLEAN | 5 | 1 |
| FadeB6 | BOOLEAN | 5 | 1 |
| FadeC6 | BOOLEAN | 5 | 1 |
| FadeD6 | BOOLEAN | 5 | 1 |
| FadeE6 | BOOLEAN | 5 | 1 |
| FadeF6 | BOOLEAN | 5 | 1 |
| FadeG6 | BOOLEAN | 5 | 1 |
| FadeH6 | BOOLEAN | 5 | 1 |
| DescrA6 | CLOB | 60 | 1 |
| DescrB6 | CLOB | 60 | 1 |
| DescrC6 | CLOB | 60 | 1 |
| DescrD6 | CLOB | 60 | 1 |
| DescrE6 | CLOB | 60 | 1 |
| DescrF6 | CLOB | 60 | 1 |
| DescrG6 | CLOB | 60 | 1 |
| DescrH6 | CLOB | 60 | 1 |
| ProdNumA6 | CLOB | 20 | 1 |
| ProdNumB6 | CLOB | 20 | 1 |
| ProdNumC6 | CLOB | 20 | 1 |
| ProdNumD6 | CLOB | 20 | 1 |
| ProdNumE6 | CLOB | 20 | 1 |
| ProdNumF6 | CLOB | 20 | 1 |
| ProdNumG6 | CLOB | 20 | 1 |
| ProdNumH6 | CLOB | 20 | 1 |
| FloodA6 | BOOLEAN | 5 | 1 |
| FloodB6 | BOOLEAN | 5 | 1 |
| FloodC6 | BOOLEAN | 5 | 1 |
| FloodD6 | BOOLEAN | 5 | 1 |
| FloodE6 | BOOLEAN | 5 | 1 |
| FloodF6 | BOOLEAN | 5 | 1 |
| FloodG6 | BOOLEAN | 5 | 1 |
| FloodH6 | BOOLEAN | 5 | 1 |
| FlopA6 | BOOLEAN | 5 | 1 |
| FlopB6 | BOOLEAN | 5 | 1 |
| FlopC6 | BOOLEAN | 5 | 1 |
| FlopD6 | BOOLEAN | 5 | 1 |
| FlopE6 | BOOLEAN | 5 | 1 |
| FlopF6 | BOOLEAN | 5 | 1 |
| FlopG6 | BOOLEAN | 5 | 1 |
| FlopH6 | BOOLEAN | 5 | 1 |
| StnA6 | CLOB | 20 | 1 |
| StnB6 | CLOB | 20 | 1 |
| StnC6 | CLOB | 20 | 1 |
| StnD6 | CLOB | 20 | 1 |
| StnE6 | CLOB | 20 | 1 |
| StnF6 | CLOB | 20 | 1 |
| StnG6 | CLOB | 20 | 1 |
| StnH6 | CLOB | 20 | 1 |
| AnaloxA6 | CLOB | 20 | 1 |
| AnaloxB6 | CLOB | 20 | 1 |
| AnaloxC6 | CLOB | 20 | 1 |
| AnaloxD6 | CLOB | 20 | 1 |
| AnaloxE6 | CLOB | 20 | 1 |
| AnaloxF6 | CLOB | 20 | 1 |
| AnaloxG6 | CLOB | 20 | 1 |
| AnaloxH6 | CLOB | 20 | 1 |
| BladeA6 | BOOLEAN | 5 | 1 |
| BladeB6 | BOOLEAN | 5 | 1 |
| BladeC6 | BOOLEAN | 5 | 1 |
| BladeD6 | BOOLEAN | 5 | 1 |
| BladeE6 | BOOLEAN | 5 | 1 |
| BladeF6 | BOOLEAN | 5 | 1 |
| BladeG6 | BOOLEAN | 5 | 1 |
| BladeH6 | BOOLEAN | 5 | 1 |
| DensityA6 | CLOB | 20 | 1 |
| DensityB6 | CLOB | 20 | 1 |
| DensityC6 | CLOB | 20 | 1 |
| DensityD6 | CLOB | 20 | 1 |
| DensityE6 | CLOB | 20 | 1 |
| DensityF6 | CLOB | 20 | 1 |
| DensityG6 | CLOB | 20 | 1 |
| DensityH6 | CLOB | 20 | 1 |
| PlateGrA6 | CLOB | 20 | 1 |
| PlateGrB6 | CLOB | 20 | 1 |
| PlateGrC6 | CLOB | 20 | 1 |
| PlateGrD6 | CLOB | 20 | 1 |
| PlateGrE6 | CLOB | 20 | 1 |
| PlateGrF6 | CLOB | 20 | 1 |
| PlateGrG6 | CLOB | 20 | 1 |
| PlateGrH6 | CLOB | 20 | 1 |
| PrintsA6 | CLOB | 20 | 1 |
| PrintsB6 | CLOB | 20 | 1 |
| PrintsC6 | CLOB | 20 | 1 |
| PrintsD6 | CLOB | 20 | 1 |
| PrintsE6 | CLOB | 20 | 1 |
| PrintsF6 | CLOB | 20 | 1 |
| PrintsG6 | CLOB | 20 | 1 |
| PrintsH6 | CLOB | 20 | 1 |
| Speed7 | CLOB | 20 | 1 |
| UWTension7 | CLOB | 20 | 1 |
| INNip7 | CLOB | 20 | 1 |
| MidNip7 | CLOB | 20 | 1 |
| ExitNip7 | CLOB | 20 | 1 |
| RWTension7 | CLOB | 20 | 1 |
| PRTension7 | CLOB | 20 | 1 |
| Press7 | CLOB | 20 | 1 |
| SetUp7 | CLOB | 20 | 1 |
| SignOff7 | CLOB | 20 | 1 |
| RWDir7 | CLOB | 20 | 1 |
| DOPType7 | CLOB | 20 | 1 |
| FFStk7 | CLOB | 20 | 1 |
| ShtStk7 | CLOB | 20 | 1 |
| Boxed7 | BOOLEAN | 5 | 1 |
| QtyPer7 | CLOB | 20 | 1 |
| Acr7 | CLOB | 20 | 1 |
| d7 | BOOLEAN | 5 | 1 |
| Coll7 | BOOLEAN | 5 | 1 |
| Delivered7 | CLOB | 60 | 1 |
| IonDep8 | BOOLEAN | 5 | 1 |
| Thermal8 | BOOLEAN | 5 | 1 |
| Printtronix8 | BOOLEAN | 5 | 1 |
| Laser8 | BOOLEAN | 5 | 1 |
| Other8 | BOOLEAN | 5 | 1 |
| Foil8 | BOOLEAN | 5 | 1 |
| Crash8 | BOOLEAN | 5 | 1 |
| BuyOut8 | BOOLEAN | 5 | 1 |
| GearA8 | CLOB | 20 | 1 |
| GearB8 | CLOB | 20 | 1 |
| SpeedA8 | CLOB | 20 | 1 |
| SpeedB8 | CLOB | 20 | 1 |
| ColorA8 | CLOB | 20 | 1 |
| ColorB8 | CLOB | 20 | 1 |
| ColorC8 | CLOB | 20 | 1 |
| ColorD8 | CLOB | 20 | 1 |
| RibbonB8 | CLOB | 20 | 1 |
| RibbonC8 | CLOB | 20 | 1 |
| Affix9 | BOOLEAN | 5 | 1 |
| FoldA9 | BOOLEAN | 5 | 1 |
| Trim9 | BOOLEAN | 5 | 1 |
| Burst9 | BOOLEAN | 5 | 1 |
| Other9 | BOOLEAN | 5 | 1 |
| Foil9 | BOOLEAN | 5 | 1 |
| Emboss9 | BOOLEAN | 5 | 1 |
| DieCut9 | BOOLEAN | 5 | 1 |
| Collate9 | BOOLEAN | 5 | 1 |
| Number9 | BOOLEAN | 5 | 1 |
| TipOn9 | BOOLEAN | 5 | 1 |
| Pad9 | BOOLEAN | 5 | 1 |
| Glue9 | BOOLEAN | 5 | 1 |
| FoldB9 | BOOLEAN | 5 | 1 |
| Drill9 | BOOLEAN | 5 | 1 |
| String9 | BOOLEAN | 5 | 1 |
| Perf9 | BOOLEAN | 5 | 1 |
| HandA9 | BOOLEAN | 5 | 1 |
| HandB9 | BOOLEAN | 5 | 1 |
| HandC9 | BOOLEAN | 5 | 1 |
| HandD9 | BOOLEAN | 5 | 1 |
| MachA9 | BOOLEAN | 5 | 1 |
| MachB9 | BOOLEAN | 5 | 1 |
| MachC9 | BOOLEAN | 5 | 1 |
| MachD9 | BOOLEAN | 5 | 1 |
| EquipA9 | CLOB | 20 | 1 |
| EquipB9 | CLOB | 20 | 1 |
| EquipC9 | CLOB | 20 | 1 |
| EquipD9 | CLOB | 20 | 1 |
| NumOfA9 | CLOB | 20 | 1 |
| NumOfB9 | CLOB | 20 | 1 |
| NumOfC9 | CLOB | 20 | 1 |
| NumOfD9 | CLOB | 20 | 1 |
| PosA9 | CLOB | 20 | 1 |
| PosB9 | CLOB | 20 | 1 |
| PosC9 | CLOB | 20 | 1 |
| PosD9 | CLOB | 20 | 1 |
| FinSzA9 | CLOB | 20 | 1 |
| FinSzB9 | CLOB | 20 | 1 |
| FinSzC9 | CLOB | 20 | 1 |
| FinSzD9 | CLOB | 20 | 1 |
| BuyVendA10 | CLOB | 20 | 1 |
| BuyVendB10 | CLOB | 20 | 1 |
| BuyVendC10 | CLOB | 20 | 1 |
| BuyVendD10 | CLOB | 20 | 1 |
| Diam10 | CLOB | 20 | 1 |
| JobDescr10 | CLOB | 0 | 1 |
| Dir10 | CLOB | 20 | 1 |
| Roll10 | BOOLEAN | 5 | 1 |
| PinF10 | BOOLEAN | 5 | 1 |
| FF10 | BOOLEAN | 5 | 1 |
| Stks10 | BOOLEAN | 5 | 1 |
| Roll11 | BOOLEAN | 5 | 1 |
| FanFold11 | BOOLEAN | 5 | 1 |
| Sheets11 | BOOLEAN | 5 | 1 |
| ACRA11 | CLOB | 20 | 1 |
| ACRB11 | CLOB | 20 | 1 |
| ACRC11 | CLOB | 20 | 1 |
| RemPinFA11 | BOOLEAN | 5 | 1 |
| RemPinFB11 | BOOLEAN | 5 | 1 |
| RemPinFC11 | BOOLEAN | 5 | 1 |
| FinWebA11 | CLOB | 20 | 1 |
| FinWebB11 | CLOB | 20 | 1 |
| FinWebC11 | CLOB | 20 | 1 |
| EquipA11 | CLOB | 20 | 1 |
| EquipB11 | CLOB | 20 | 1 |
| EquipC11 | CLOB | 20 | 1 |
| DirA11 | CLOB | 20 | 1 |
| DirB11 | CLOB | 20 | 1 |
| DirC11 | CLOB | 20 | 1 |
| QtyPerA11 | CLOB | 20 | 1 |
| QtypPerB11 | CLOB | 20 | 1 |
| QtyPerC11 | CLOB | 20 | 1 |
| ATONA11 | CLOB | 20 | 1 |
| ATONB11 | CLOB | 20 | 1 |
| CountA11 | CLOB | 20 | 1 |
| CountB11 | CLOB | 20 | 1 |
| DiamA11 | CLOB | 20 | 1 |
| DiamB11 | CLOB | 20 | 1 |
| LblsAcr11 | CLOB | 20 | 1 |
| LblsDwn11 | CLOB | 20 | 1 |
| LblsStk11 | CLOB | 20 | 1 |
| CoreMks11 | CLOB | 20 | 1 |
| FlagOk11 | BOOLEAN | 5 | 1 |
| SpliceOK11 | BOOLEAN | 5 | 1 |
| Bulk11 | BOOLEAN | 5 | 1 |
| Band11 | BOOLEAN | 5 | 1 |
| Chip11 | BOOLEAN | 5 | 1 |
| PolyBag11 | BOOLEAN | 5 | 1 |
| Shrink11 | BOOLEAN | 5 | 1 |
| PlantOpt12 | BOOLEAN | 5 | 1 |
| Consist12 | BOOLEAN | 5 | 1 |
| LblStks12 | BOOLEAN | 5 | 1 |
| StoreExtras12 | BOOLEAN | 5 | 1 |
| ReqdPack12 | BOOLEAN | 5 | 1 |
| RollsStks12 | CLOB | 20 | 1 |
| BoxSize12 | CLOB | 20 | 1 |
| RollStksb12 | CLOB | 20 | 1 |
| BoxSizeb12 | CLOB | 20 | 1 |
| Weight12 | CLOB | 20 | 1 |
| CartonQty12 | CLOB | 20 | 1 |
| Lbls12 | BOOLEAN | 5 | 1 |
| Stks12 | BOOLEAN | 5 | 1 |
| Instruction13 | BOOLEAN | 5 | 1 |
| LWLabel13 | BOOLEAN | 5 | 1 |
| Distributor13 | BOOLEAN | 5 | 1 |
| CustLabel13 | BOOLEAN | 5 | 1 |
| CustPS13 | BOOLEAN | 5 | 1 |
| Cert13 | BOOLEAN | 5 | 1 |
| BigText | CLOB | 0 | 1 |
| FinSheet | CLOB | 20 | 1 |
| FinForm | CLOB | 20 | 1 |
| PolyBag11b | BOOLEAN | 5 | 1 |
| PolyBag11c | BOOLEAN | 5 | 1 |
| Shrink11b | BOOLEAN | 5 | 1 |
| Shrink11c | BOOLEAN | 5 | 1 |
| PK_UUID | UUID | 0 | 1 |

### Labels

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| Printer | CLOB | 30 | 1 |
| Label_Name | CLOB | 60 | 1 |
| Label_Text_Form | CLOB | 0 | 1 |
| LHX | CLOB | 20 | 1 |
| LHY | CLOB | 20 | 1 |
| AssocFile | INT16 | 6 | 1 |
| PK_UUID | UUID | 0 | 1 |

### Language_Item

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| Resource_Name | CLOB | 0 | 1 |
| Resource_Number | INT32 | 11 | 1 |
| Item_Number | INT32 | 11 | 1 |
| Definition | CLOB | 0 | 1 |
| Language_1 | CLOB | 0 | 1 |
| Language_2 | CLOB | 0 | 1 |
| Language_3 | CLOB | 0 | 1 |
| Language_4 | CLOB | 0 | 1 |
| Language_5 | CLOB | 0 | 1 |
| Language_6 | CLOB | 0 | 1 |
| Language_7 | CLOB | 0 | 1 |
| Length_1 | INT32 | 11 | 1 |
| Length_2 | INT32 | 11 | 1 |
| Length_3 | INT32 | 11 | 1 |
| Length_4 | INT32 | 11 | 1 |
| Length_5 | INT32 | 11 | 1 |
| Length_6 | INT32 | 11 | 1 |
| Length_7 | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |

### Large_Objects

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| Related_Table | INT32 | 11 | 1 |
| Related_ID | INT32 | 11 | 1 |
| Blob_Object | BLOB | 0 | 1 |
| Source_Application | CLOB | 30 | 1 |
| File_Name | CLOB | 30 | 1 |
| QuoteLetter_ | BLOB | 0 | 1 |
| Reference | CLOB | 255 | 1 |
| PK_UUID | UUID | 0 | 1 |
| JSON_4D | None | 0 | 1 |

### Launch_History

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| Database_State | CLOB | 30 | 1 |
| StartUp_TimeStamp | CLOB | 80 | 1 |
| ShutDown_TimeStamp | CLOB | 80 | 1 |
| PK_UUID | UUID | 0 | 1 |

### List

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| GroupName | CLOB | 40 | 1 |
| Name | CLOB | 255 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### Logs

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| Log_Name | CLOB | 30 | 1 |
| Log_Text | CLOB | 0 | 1 |
| LastModDate | TIMESTAMP | 19 | 1 |
| LastModTime | INTERVAL | 10 | 1 |
| PK_UUID | UUID | 0 | 1 |

### MFGRep

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| Number | CLOB | 10 | 1 |
| Company | CLOB | 80 | 1 |
| Honorific_Prefix | CLOB | 10 | 1 |
| FirstName | CLOB | 10 | 1 |
| LastName | CLOB | 20 | 1 |
| Addr1 | CLOB | 255 | 1 |
| Addr2 | CLOB | 255 | 1 |
| City | CLOB | 40 | 1 |
| State_Province | CLOB | 25 | 1 |
| Zip | CLOB | 15 | 1 |
| Phone | CLOB | 20 | 1 |
| FAX | CLOB | 20 | 1 |
| CommPrcnt | REAL | 7 | 1 |
| Notes | CLOB | 0 | 1 |
| Inactive | BOOLEAN | 5 | 1 |
| Email | CLOB | 60 | 1 |
| EnteredBy | CLOB | 50 | 1 |
| ModifiedBy | CLOB | 50 | 1 |
| EnteredDate | TIMESTAMP | 19 | 1 |
| ModifiedDate | TIMESTAMP | 19 | 1 |
| EnteredTime | INTERVAL | 10 | 1 |
| ModifiedTime | INTERVAL | 10 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |
| Tag | CLOB | 3 | 1 |

### Maintenance

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| EquipNumber | CLOB | 10 | 1 |
| mDate | TIMESTAMP | 19 | 1 |
| Description | CLOB | 80 | 1 |
| Cost | REAL | 7 | 1 |
| PerformedBy | CLOB | 30 | 1 |
| Notes | CLOB | 0 | 1 |
| PK_UUID | UUID | 0 | 1 |

### MarketingCategory

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| CustomerID | CLOB | 10 | 1 |
| Category | CLOB | 80 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### MasterInvoice_Detail

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| InvoiceNumber | CLOB | 10 | 1 |
| iDate | TIMESTAMP | 19 | 1 |
| TicketNum | CLOB | 12 | 1 |
| CustomerNumber | CLOB | 10 | 1 |
| CustomerName | CLOB | 40 | 1 |
| CustomerPO_Num | CLOB | 25 | 1 |
| InvBalance | REAL | 7 | 1 |
| IncludeInMaster | BOOLEAN | 5 | 1 |
| MasterInvoiceNumber | CLOB | 10 | 1 |
| STotalDiscount | REAL | 7 | 1 |
| PlateCharge | REAL | 7 | 1 |
| ColorCharge | REAL | 7 | 1 |
| PurchItems | REAL | 7 | 1 |
| STotal | REAL | 7 | 1 |
| Misc | REAL | 7 | 1 |
| Freight | REAL | 7 | 1 |
| Tax | REAL | 7 | 1 |
| Tax2 | REAL | 7 | 1 |
| Total | REAL | 7 | 1 |
| TotalPaid | REAL | 7 | 1 |
| Discount | REAL | 7 | 1 |
| Balance | REAL | 7 | 1 |
| SalesCommissionAmount | REAL | 7 | 1 |
| PO_Art | REAL | 7 | 1 |
| PO_Plate | REAL | 7 | 1 |
| PO_Tool | REAL | 7 | 1 |
| PO_Generic | REAL | 7 | 1 |
| AR_Transaction_ID | INT32 | 11 | 1 |
| TaxAmount_Total | REAL | 7 | 1 |
| Currency_ID | INT32 | 11 | 1 |
| Currency_ExchangeRate | REAL | 7 | 1 |
| FC_TaxTotal | REAL | 7 | 1 |
| FC_SP_Discount | REAL | 7 | 1 |
| FC_PlateCharge | REAL | 7 | 1 |
| FC_ColorCharge | REAL | 7 | 1 |
| FC_Total | REAL | 7 | 1 |
| MFGRepCommAmount | REAL | 7 | 1 |
| FC_PurchItems | REAL | 7 | 1 |
| FC_PO_Art | REAL | 7 | 1 |
| FC_PO_Plate | REAL | 7 | 1 |
| FC_PO_Tool | REAL | 7 | 1 |
| FC_PO_Generic | REAL | 7 | 1 |
| FC_STotal | REAL | 7 | 1 |
| FC_Misc | REAL | 7 | 1 |
| FC_Freight | REAL | 7 | 1 |
| FC_TotalPaid | REAL | 7 | 1 |
| FC_Balance | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |

### MasterInvoice_POs

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| MasterInvoiceNumber | CLOB | 10 | 1 |
| TicketNum | CLOB | 12 | 1 |
| PO_Number | CLOB | 10 | 1 |
| PO_Type | CLOB | 20 | 1 |
| SupplierNum | CLOB | 10 | 1 |
| SupplierName | CLOB | 80 | 1 |
| PO_Date | TIMESTAMP | 19 | 1 |
| PO_Description | CLOB | 50 | 1 |
| SellPrice | REAL | 7 | 1 |
| InvoiceNum | CLOB | 10 | 1 |
| FC_Customer_SellPrice | REAL | 7 | 1 |
| FC_Customer_Currency_ID | INT32 | 11 | 1 |
| FC_Customer_Currency_Rate_ID | INT32 | 11 | 1 |
| FC_Customer_ExchangeRate | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |

### Material_Use

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| Inventory_ID | CLOB | 10 | 1 |
| Part_Number | CLOB | 40 | 1 |
| Ticket_ID | CLOB | 10 | 1 |
| TicketStock_ID | INT32 | 11 | 1 |
| PO_ID | INT32 | 11 | 1 |
| PO_Item_ID | CLOB | 10 | 1 |
| BillCode | INT32 | 11 | 1 |
| u2 | CLOB | 0 | 1 |
| Date_Posted | TIMESTAMP | 19 | 1 |
| Time_Posted | INTERVAL | 10 | 1 |
| PostedTimeStamp | INT32 | 11 | 1 |
| Depart_ID | INT32 | 11 | 1 |
| Depart_Name | CLOB | 20 | 1 |
| Equip_ID | CLOB | 10 | 1 |
| Equip_Name | CLOB | 40 | 1 |
| Employee_ID | CLOB | 10 | 1 |
| EmployeeFName | CLOB | 20 | 1 |
| EmployeeLName | CLOB | 20 | 1 |
| Quantity | REAL | 7 | 1 |
| Fixed_Unit | CLOB | 20 | 1 |
| Fixed_UnitCost | REAL | 7 | 1 |
| No_Out_Stock | INT32 | 11 | 1 |
| File_ID_Ref | CLOB | 15 | 1 |
| Notes | CLOB | 0 | 1 |
| u3 | CLOB | 0 | 1 |
| Fixed_Unit_Local | CLOB | 20 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### MenuReports

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| PK_UUID | UUID | 0 | 0 |
| Menu_Category | CLOB | 0 | 1 |
| MethodToExecute | CLOB | 0 | 1 |
| ParameterToMethod | CLOB | 255 | 1 |
| ReportName | CLOB | 0 | 1 |
| Description | CLOB | 0 | 1 |
| TableNo | INT32 | 11 | 1 |
| FieldNo | INT32 | 11 | 1 |
| TableNoDescr | INT32 | 11 | 1 |
| FieldNoDescr | INT32 | 11 | 1 |

### OAuth2

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| PK_UUID | UUID | 0 | 0 |
| provider | None | 0 | 1 |
| userAccount | CLOB | 255 | 1 |
| providerType | CLOB | 255 | 1 |
| associateNumber | CLOB | 10 | 1 |

### POItems

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| PO_ID | CLOB | 10 | 1 |
| Quantity | REAL | 7 | 1 |
| Description | CLOB | 0 | 1 |
| Received | TIMESTAMP | 19 | 1 |
| Unit | CLOB | 20 | 1 |
| Unit_Cost | REAL | 7 | 1 |
| LineTotal | REAL | 7 | 1 |
| Receive_Qty | REAL | 7 | 1 |
| Part_Type | CLOB | 30 | 1 |
| Part_Number | CLOB | 40 | 1 |
| Complete | BOOLEAN | 5 | 1 |
| VendorPartNo | CLOB | 40 | 1 |
| Return_POItemID | CLOB | 10 | 1 |
| Received_Total | REAL | 7 | 1 |
| Is_StockProduct | BOOLEAN | 5 | 1 |
| Unit_Local | CLOB | 20 | 1 |
| PK_UUID | UUID | 0 | 1 |
| FC_Unit_Cost | REAL | 7 | 1 |
| FC_LineTotal | REAL | 7 | 1 |
| FC_Received_Total | REAL | 7 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### PO_Item_Stock

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| PO_Number | CLOB | 10 | 1 |
| OrderFootage | INT32 | 11 | 1 |
| ReceiveFootage | INT32 | 11 | 1 |
| RollNum | INT32 | 11 | 1 |
| Cut1 | REAL | 7 | 1 |
| Cut2 | REAL | 7 | 1 |
| Cut3 | REAL | 7 | 1 |
| Cut4 | REAL | 7 | 1 |
| Cut5 | REAL | 7 | 1 |
| NumCut1 | INT32 | 11 | 1 |
| NumCut2 | INT32 | 11 | 1 |
| NumCut3 | INT32 | 11 | 1 |
| NumCut4 | INT32 | 11 | 1 |
| NumCut5 | INT32 | 11 | 1 |
| RollOffCut | REAL | 7 | 1 |
| EntryDate | TIMESTAMP | 19 | 1 |
| EntryBy | CLOB | 50 | 1 |
| ModifyDate | TIMESTAMP | 19 | 1 |
| ModifyBy | CLOB | 50 | 1 |
| ReceiptBatchID | INT32 | 11 | 1 |
| ReceiveDate | TIMESTAMP | 19 | 1 |
| ReceiptBatchStatus | CLOB | 20 | 1 |
| PushPORecToAP_Status | CLOB | 20 | 1 |
| AP_Invoice_ID | INT32 | 11 | 1 |
| FassonOnOrder | CLOB | 10 | 1 |
| ExactWidths | BOOLEAN | 5 | 1 |
| EntryTime | INTERVAL | 10 | 1 |
| ModifyTime | INTERVAL | 10 | 1 |
| PK_UUID | UUID | 0 | 1 |
| Weight | REAL | 7 | 1 |
| Diameter_Outer | REAL | 7 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |
| Received | BOOLEAN | 5 | 1 |

### PO_Stock_PackListXML

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| PO_Stock_eReceiptShipID | INT32 | 11 | 1 |
| XML_Source | BLOB | 0 | 1 |
| PK_UUID | UUID | 0 | 1 |

### PO_Stock_eReceiptRolls

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| Ship_ID | INT32 | 11 | 1 |
| Fasson_Roll_ID | CLOB | 60 | 1 |
| Roll_Width | REAL | 7 | 1 |
| Roll_Length | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |

### PO_Stock_eReceiptShip

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| PO_Number | CLOB | 10 | 1 |
| ePackSlipShipNum | CLOB | 80 | 1 |
| ShipDate | TIMESTAMP | 19 | 1 |
| ShipVia | CLOB | 40 | 1 |
| ShipComplete | CLOB | 80 | 1 |
| ReceiptBatchID | INT32 | 11 | 1 |
| ReceiveDate | TIMESTAMP | 19 | 1 |
| ReceiptBatchStatus | CLOB | 20 | 1 |
| PushPORecToAP_Status | CLOB | 20 | 1 |
| AP_Invoice_ID | INT32 | 11 | 1 |
| x | CLOB | 0 | 1 |
| SupplierCustomerNumber | CLOB | 25 | 1 |
| ePackingSlipDate | TIMESTAMP | 19 | 1 |
| PK_UUID | UUID | 0 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |

### PackSlipItem

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| PackSlipNumber | CLOB | 10 | 1 |
| ProductNumber | CLOB | 30 | 1 |
| TicketItemID | CLOB | 10 | 1 |
| OrderQuantity | INT32 | 11 | 1 |
| ShipQuantity | INT32 | 11 | 1 |
| BackOrdered | INT32 | 11 | 1 |
| PricePerM | REAL | 7 | 1 |
| InvShipped | INT32 | 11 | 1 |
| ProdDescr | CLOB | 80 | 1 |
| Complete | BOOLEAN | 5 | 1 |
| PrevShip | INT32 | 11 | 1 |
| Inventory | INT32 | 11 | 1 |
| OverRun | INT32 | 11 | 1 |
| ConsecNo | CLOB | 20 | 1 |
| PriceMode | CLOB | 20 | 1 |
| ShipDelta | CLOB | 12 | 1 |
| ProdDesc2 | CLOB | 80 | 1 |
| StockProduct_ID | CLOB | 10 | 1 |
| PO_Number | CLOB | 30 | 1 |
| Location | CLOB | 40 | 1 |
| PK_UUID | UUID | 0 | 1 |
| PriceMode_Local | CLOB | 20 | 1 |
| Unit_Weight | REAL | 7 | 1 |
| Order_Weight | REAL | 7 | 1 |
| Ship_Weight | REAL | 7 | 1 |
| BackOrder_Weight | REAL | 7 | 1 |
| PrevShip_Weight | REAL | 7 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### PackingSlip

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| Number | CLOB | 10 | 1 |
| Suffix | INT16 | 6 | 1 |
| ShipDate | TIMESTAMP | 19 | 1 |
| Freight | REAL | 7 | 1 |
| ShipAttn | CLOB | 30 | 1 |
| ShippingInstruc | CLOB | 50 | 1 |
| Is_BlanketOrder | CLOB | 5 | 1 |
| ContactEmail | CLOB | 60 | 1 |
| ShipLocation | CLOB | 80 | 1 |
| ShipAddr1 | CLOB | 255 | 1 |
| ShipAddr2 | CLOB | 255 | 1 |
| ShipCity | CLOB | 40 | 1 |
| ShipState | CLOB | 25 | 1 |
| ShipZip | CLOB | 15 | 1 |
| CustomerNumber | CLOB | 10 | 1 |
| Notes | CLOB | 0 | 1 |
| ShipCountry | CLOB | 25 | 1 |
| Shipped | BOOLEAN | 5 | 1 |
| TotalCost | REAL | 7 | 1 |
| TotalPaid | REAL | 7 | 1 |
| TicketNum | CLOB | 12 | 1 |
| CustomerName | CLOB | 80 | 1 |
| InvoiceNo | CLOB | 10 | 1 |
| ShipVia | CLOB | 40 | 1 |
| AssocName | CLOB | 35 | 1 |
| ShipTime | INTERVAL | 10 | 1 |
| NoPackage | INT32 | 11 | 1 |
| Weight | REAL | 7 | 1 |
| PayMethod | INT32 | 11 | 1 |
| ShipClass | CLOB | 10 | 1 |
| Complete | BOOLEAN | 5 | 1 |
| MiscChargeDesc | CLOB | 30 | 1 |
| MiscCharge | REAL | 7 | 1 |
| FromgLicense | BOOLEAN | 5 | 1 |
| SuppressFrom | BOOLEAN | 5 | 1 |
| TrackingNum | CLOB | 40 | 1 |
| SuppressZeroLines | BOOLEAN | 5 | 1 |
| Is_StockProduct | BOOLEAN | 5 | 1 |
| May_Ship_Early | BOOLEAN | 5 | 1 |
| Must_Ship_Complete | BOOLEAN | 5 | 1 |
| From_Name | CLOB | 80 | 1 |
| From_Address1 | CLOB | 255 | 1 |
| From_Address2 | CLOB | 255 | 1 |
| From_City | CLOB | 40 | 1 |
| From_State | CLOB | 25 | 1 |
| From_Zip | CLOB | 15 | 1 |
| From_Country | CLOB | 25 | 1 |
| Ship_Terms | CLOB | 45 | 1 |
| InvoiceNow | BOOLEAN | 5 | 1 |
| EnteredDate | TIMESTAMP | 19 | 1 |
| ModifiedBy | CLOB | 50 | 1 |
| ModifiedDate | TIMESTAMP | 19 | 1 |
| StockProductLink_SPL | CLOB | 5 | 1 |
| DontPrintTerms | BOOLEAN | 5 | 1 |
| Ship_Address_ID | CLOB | 10 | 1 |
| Ship_TaxRegion_ID | INT32 | 11 | 1 |
| EnteredBy | CLOB | 50 | 1 |
| EnteredTime | INTERVAL | 10 | 1 |
| ModifiedTime | INTERVAL | 10 | 1 |
| SendEmailAlert | BOOLEAN | 5 | 1 |
| Freight_AcctNo | CLOB | 20 | 1 |
| ReceivedFromUPSSDate | TIMESTAMP | 19 | 1 |
| ReceivedFromUPSSTime | INTERVAL | 10 | 1 |
| SentToUPSSDate | TIMESTAMP | 19 | 1 |
| SentToUPSSTime | INTERVAL | 10 | 1 |
| TypeOfOrder | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |
| Tag | CLOB | 255 | 1 |
| masterPSID | CLOB | 10 | 1 |
| batchLocation | CLOB | 40 | 1 |
| batchPalletID | CLOB | 20 | 1 |
| mixed | BOOLEAN | 5 | 1 |
| Origin_Tag | CLOB | 3 | 1 |

### Patch_History

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| PatchRun_Date | TIMESTAMP | 19 | 1 |
| PatchRun_Time | INTERVAL | 10 | 1 |
| Run_Version | CLOB | 40 | 1 |
| Run_BuildNumber | CLOB | 40 | 1 |
| Patch_MethodName | CLOB | 40 | 1 |
| Patch_Date | TIMESTAMP | 19 | 1 |
| Patch_Message | CLOB | 80 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### Payment

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| InvoiceNumber | CLOB | 10 | 1 |
| CustomerNumber | CLOB | 10 | 1 |
| TicketNumber | CLOB | 12 | 1 |
| PDate | TIMESTAMP | 19 | 1 |
| Amount | REAL | 7 | 1 |
| Notes | CLOB | 0 | 1 |
| PartPay | BOOLEAN | 5 | 1 |
| Discount | REAL | 7 | 1 |
| Balance | REAL | 7 | 1 |
| Misc | REAL | 7 | 1 |
| CopiedToNewCR | CLOB | 5 | 1 |
| PK_UUID | UUID | 0 | 1 |

### Payment_Terms

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| Description | CLOB | 45 | 1 |
| NetDayDue | INT32 | 11 | 1 |
| DiscountPercent | REAL | 7 | 1 |
| DiscountDays | INT32 | 11 | 1 |
| Default_Term | BOOLEAN | 5 | 1 |
| Inactive | BOOLEAN | 5 | 1 |
| EndOfMonthDueDate | BOOLEAN | 5 | 1 |
| EndOfMonthDiscountDate | BOOLEAN | 5 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### Pop_Localization

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 0 | 1 |
| popup_Name | CLOB | 0 | 1 |
| Orig_Value | CLOB | 0 | 1 |
| Form_No | INT32 | 11 | 1 |
| Item_No | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |

### PostPress_LineItem

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| Equip_Number | CLOB | 10 | 1 |
| Operation_Desc | CLOB | 40 | 1 |
| PiecesOperation | INT32 | 11 | 1 |
| Operations_Hour | INT32 | 11 | 1 |
| Material_Desc | CLOB | 40 | 1 |
| Material_Rate | REAL | 7 | 1 |
| Material_Unit | CLOB | 20 | 1 |
| PK_UUID | UUID | 0 | 1 |
| Weight_Piece | REAL | 7 | 1 |

### Press_Sensor_Status

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| Sensor_SerialNumber | CLOB | 40 | 1 |
| WorkStation_Name | CLOB | 80 | 1 |
| Equipment_Number | CLOB | 10 | 1 |
| Roll_1_IDNumber | CLOB | 60 | 1 |
| Roll_2_IDNumber | CLOB | 60 | 1 |
| Roll_3_IDNumber | CLOB | 60 | 1 |
| AssocNum | CLOB | 10 | 1 |
| Last_TimeCard_Operation | CLOB | 20 | 1 |
| Ticket_Number | CLOB | 12 | 1 |
| Job_Start_DateTime | INT32 | 11 | 1 |
| Job_Start_Counter | REAL | 7 | 1 |
| Job_Start_IsProduction | BOOLEAN | 5 | 1 |
| MidPoint_DateTime | INT32 | 11 | 1 |
| MidPoint_Counter | REAL | 7 | 1 |
| MidPoint_IsProduction | BOOLEAN | 5 | 1 |
| EndPoint_DateTime | INT32 | 11 | 1 |
| EndPoint_Counter | REAL | 7 | 1 |
| EndPoint_IsProduction | BOOLEAN | 5 | 1 |
| MakeReady_Start_DateTime | INT32 | 11 | 1 |
| MakeReady_End_DateTime | INT32 | 11 | 1 |
| Run_Start_DateTime | INT32 | 11 | 1 |
| Run_Start_Counter | REAL | 7 | 1 |
| WashUp_Start_DateTime | INT32 | 11 | 1 |
| WashUp_Start_Counter | REAL | 7 | 1 |
| Waste_Counter | REAL | 7 | 1 |
| Production_Counter | REAL | 7 | 1 |
| Roll_1_Start_Count | REAL | 7 | 1 |
| Roll_2_Start_Count | REAL | 7 | 1 |
| Roll_3_Start_Count | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |

### Price

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| StockProdID | CLOB | 10 | 1 |
| CustomerID | CLOB | 10 | 1 |
| Qty | INT32 | 11 | 1 |
| Cost | REAL | 7 | 1 |
| SalePrice | REAL | 7 | 1 |
| Distributor | BOOLEAN | 5 | 1 |
| GroupName | CLOB | 40 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### Prod_AddlStock

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| UniqueProductID | CLOB | 10 | 1 |
| StockNum | CLOB | 10 | 1 |
| Width | REAL | 7 | 1 |
| Description | CLOB | 40 | 1 |
| Caliper | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |
| RoutingNo | INT16 | 6 | 1 |

### Prod_UserDefined

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| EquipUserDefined_ID | INT32 | 11 | 1 |
| UniqueProductID | CLOB | 10 | 1 |
| Description | CLOB | 20 | 1 |
| UseThisOption | BOOLEAN | 5 | 1 |
| Notes | CLOB | 60 | 1 |
| Print_On_Reports | BOOLEAN | 5 | 1 |
| Order_in_List | INT32 | 11 | 1 |
| Press_Number | CLOB | 10 | 1 |
| Option_Multiplier | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### Product

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ProdNum | CLOB | 30 | 1 |
| CustNum | CLOB | 10 | 1 |
| ProdNum_CustNum | CLOB | 40 | 1 |
| Description | CLOB | 80 | 1 |
| ProdDate | TIMESTAMP | 19 | 1 |
| ColorDescr | CLOB | 80 | 1 |
| JobType | CLOB | 4 | 1 |
| MaterialTrac | BOOLEAN | 5 | 1 |
| AutoAppl | BOOLEAN | 5 | 1 |
| ProdGroup | CLOB | 40 | 1 |
| SizeAcross | REAL | 7 | 1 |
| SizeAround | REAL | 7 | 1 |
| ColSpace | REAL | 7 | 1 |
| RowSpace | REAL | 7 | 1 |
| LabelRepeat | REAL | 7 | 1 |
| NoAcross | INT16 | 6 | 1 |
| NoAround | INT16 | 6 | 1 |
| CSA | BOOLEAN | 5 | 1 |
| FinishType | CLOB | 15 | 1 |
| Pinfeed | BOOLEAN | 5 | 1 |
| LabelsPer_ | INT32 | 11 | 1 |
| NoLabAcrossFin | INT16 | 6 | 1 |
| CoreDiameter | REAL | 7 | 1 |
| FinalUnwind | CLOB | 15 | 1 |
| LabelsPerFold | INT16 | 6 | 1 |
| Notes | CLOB | 0 | 1 |
| Tab | REAL | 7 | 1 |
| Press | CLOB | 10 | 1 |
| TotalTickets | INT16 | 6 | 1 |
| CornerRadius | REAL | 7 | 1 |
| TurnBar | BOOLEAN | 5 | 1 |
| InkType | CLOB | 10 | 1 |
| NoOfColors | INT16 | 6 | 1 |
| ColumnPerf | REAL | 7 | 1 |
| RowPerf | REAL | 7 | 1 |
| Plate_ID | CLOB | 60 | 1 |
| EstimateNum | CLOB | 10 | 1 |
| Quantity1 | INT32 | 11 | 1 |
| PricePerM1 | REAL | 7 | 1 |
| Quantity2 | INT32 | 11 | 1 |
| PricePerM2 | REAL | 7 | 1 |
| Quantity3 | INT32 | 11 | 1 |
| PricePerM3 | REAL | 7 | 1 |
| Quantity4 | INT32 | 11 | 1 |
| PricePerM4 | REAL | 7 | 1 |
| Quantity5 | INT32 | 11 | 1 |
| PricePerM5 | REAL | 7 | 1 |
| Quantity6 | INT32 | 11 | 1 |
| PricePerM6 | REAL | 7 | 1 |
| EndUserNum | CLOB | 10 | 1 |
| StockNum1 | CLOB | 10 | 1 |
| StockWidth1 | REAL | 7 | 1 |
| StockNum2 | CLOB | 10 | 1 |
| StockWidth2 | REAL | 7 | 1 |
| StockNum3 | CLOB | 10 | 1 |
| StockWidth3 | REAL | 7 | 1 |
| SheetPackType | CLOB | 15 | 1 |
| NoTickets | INT32 | 11 | 1 |
| NoFloods | INT16 | 6 | 1 |
| ToolNo1 | CLOB | 15 | 1 |
| ToolNo2 | CLOB | 15 | 1 |
| Tool2Descr | CLOB | 15 | 1 |
| ToolNo3 | CLOB | 15 | 1 |
| Tool3Descr | CLOB | 15 | 1 |
| ToolNo4 | CLOB | 15 | 1 |
| Tool4Descr | CLOB | 15 | 1 |
| ToolNo5 | CLOB | 15 | 1 |
| Tool5Descr | CLOB | 20 | 1 |
| ConsecNo | CLOB | 20 | 1 |
| Shape | CLOB | 40 | 1 |
| CustName | CLOB | 80 | 1 |
| EndUserName | CLOB | 80 | 1 |
| StockDescr1 | CLOB | 80 | 1 |
| StockDescr2 | CLOB | 80 | 1 |
| StockDescr3 | CLOB | 80 | 1 |
| CarrierWidth | REAL | 7 | 1 |
| Inventory | INT32 | 11 | 1 |
| OverRun | INT32 | 11 | 1 |
| Hidden_Notes | CLOB | 0 | 1 |
| ProjOrder | TIMESTAMP | 19 | 1 |
| ProjectProd | BOOLEAN | 5 | 1 |
| TabPosition | BOOLEAN | 5 | 1 |
| CustIsDistrib | BOOLEAN | 5 | 1 |
| UL | BOOLEAN | 5 | 1 |
| PriceMode | CLOB | 20 | 1 |
| MiscChargeDesc | CLOB | 30 | 1 |
| MiscCharge | REAL | 7 | 1 |
| CoreType | CLOB | 15 | 1 |
| RollLength | INT32 | 11 | 1 |
| RollUnit | CLOB | 7 | 1 |
| Tape | BOOLEAN | 5 | 1 |
| Commission | REAL | 7 | 1 |
| SpecialPrice | BOOLEAN | 5 | 1 |
| BC_Symbol | CLOB | 30 | 1 |
| BC_Height | REAL | 7 | 1 |
| BC_Width | REAL | 7 | 1 |
| BC_XDim | REAL | 7 | 1 |
| BC_DataOrigin | CLOB | 15 | 1 |
| BC_Ratio | CLOB | 30 | 1 |
| BC_Prefix | BOOLEAN | 5 | 1 |
| BC_CheckDigit | BOOLEAN | 5 | 1 |
| BC_Start | CLOB | 20 | 1 |
| BC_End | CLOB | 20 | 1 |
| BC_HRStart | CLOB | 20 | 1 |
| BC_HREnd | CLOB | 20 | 1 |
| BC_Position | CLOB | 30 | 1 |
| CostField | REAL | 7 | 1 |
| UserDef_MR_1 | BOOLEAN | 5 | 1 |
| UserDef_MR_2 | BOOLEAN | 5 | 1 |
| UserDef_MR_1_Lb | CLOB | 20 | 1 |
| USerDef_MR_2_Lb | CLOB | 20 | 1 |
| OutsideDiameter | REAL | 7 | 1 |
| Caliper_Laminat | REAL | 7 | 1 |
| Caliper_FaceStk | REAL | 7 | 1 |
| Caliper_Adhesiv | REAL | 7 | 1 |
| FinishNotes | CLOB | 80 | 1 |
| UniqueProdID | CLOB | 10 | 1 |
| Name1 | CLOB | 80 | 1 |
| Name2 | CLOB | 80 | 1 |
| Name3 | CLOB | 80 | 1 |
| Name4 | CLOB | 80 | 1 |
| PopUpName1 | CLOB | 40 | 1 |
| PopUpName2 | CLOB | 40 | 1 |
| RevisionNo | CLOB | 20 | 1 |
| ToolingNotes | CLOB | 50 | 1 |
| CertificatNotes | CLOB | 50 | 1 |
| CriticalQuality | CLOB | 0 | 1 |
| CoreWidth | REAL | 7 | 1 |
| CartonSize | CLOB | 20 | 1 |
| NumPerCarton | CLOB | 20 | 1 |
| PalletSize | CLOB | 20 | 1 |
| RewindEquipNum | CLOB | 10 | 1 |
| RewindEquipNam | CLOB | 35 | 1 |
| SubProduct | BOOLEAN | 5 | 1 |
| AmortizePlateChanges | BOOLEAN | 5 | 1 |
| AmortizeColorChanges | BOOLEAN | 5 | 1 |
| StockNotes | CLOB | 0 | 1 |
| Sheet_Width | REAL | 7 | 1 |
| Sheet_Height | REAL | 7 | 1 |
| Inactive | BOOLEAN | 5 | 1 |
| SlitOnRewind | BOOLEAN | 5 | 1 |
| Image_SourceApplication | CLOB | 30 | 1 |
| Image_FileName | CLOB | 30 | 1 |
| EnteredBy | CLOB | 50 | 1 |
| ModifiedBy | CLOB | 50 | 1 |
| EnteredDate | TIMESTAMP | 19 | 1 |
| ModifiedDate | TIMESTAMP | 19 | 1 |
| EnteredTime | INTERVAL | 10 | 1 |
| ModifiedTime | INTERVAL | 10 | 1 |
| Equip_ID | CLOB | 10 | 1 |
| Are_Tools_for_Equip | BOOLEAN | 5 | 1 |
| Equip_NoColors | INT16 | 6 | 1 |
| Equip_NoFloods | INT16 | 6 | 1 |
| Group_ID | CLOB | 40 | 1 |
| Press_Null_Cycles | INT32 | 11 | 1 |
| Equip_Null_Cycles | INT32 | 11 | 1 |
| Use_TurretRewinder | BOOLEAN | 5 | 1 |
| Currency_ID | INT32 | 11 | 1 |
| Currency_ExchangeRate | REAL | 7 | 1 |
| Image_Format | INT32 | 11 | 1 |
| ShrinkSleeve_OverLap | REAL | 7 | 1 |
| ShrinkSleeve_LayFlat | REAL | 7 | 1 |
| ShrinkSleeve_CutHeight | REAL | 7 | 1 |
| CommissionSource | CLOB | 20 | 1 |
| ProfitAdjLabel | CLOB | 20 | 1 |
| SalesRepNumber | CLOB | 10 | 1 |
| SalesRepName | CLOB | 60 | 1 |
| InternetQuery | BOOLEAN | 5 | 1 |
| eTraxx_BackStagePDF | CLOB | 0 | 1 |
| Image_Size | REAL | 7 | 1 |
| BackStage_ColorStrategy | CLOB | 40 | 1 |
| BackStage_SmartMarkSet | CLOB | 40 | 1 |
| Equip3_ID | CLOB | 10 | 1 |
| Equip3_NoColors | INT16 | 6 | 1 |
| Equip3_NoFloods | INT16 | 6 | 1 |
| Equip3_Null_Cycles | INT32 | 11 | 1 |
| Equip4_ID | CLOB | 10 | 1 |
| Equip4_NoColors | INT16 | 6 | 1 |
| Equip4_NoFloods | INT16 | 6 | 1 |
| Equip4_Null_Cycles | INT32 | 11 | 1 |
| Equip_NoAcross | INT32 | 11 | 1 |
| Equip_NoAround | INT32 | 11 | 1 |
| Equip_NumUp_Multiplier | INT32 | 11 | 1 |
| Equip3_NoAcross | INT32 | 11 | 1 |
| Equip3_NoAround | INT32 | 11 | 1 |
| Equip3_NumUp_Multiplier | INT32 | 11 | 1 |
| Equip4_NoAcross | INT32 | 11 | 1 |
| Equip4_NoAround | INT32 | 11 | 1 |
| Equip4_NumUp_Multiplier | INT32 | 11 | 1 |
| JDF_Sent_On | CLOB | 40 | 1 |
| JDF_Not_Allowed | BOOLEAN | 5 | 1 |
| Tool_NumberAround | INT16 | 6 | 1 |
| Roto_Quote_Number | CLOB | 80 | 1 |
| Roto_Quote_Line_ID | CLOB | 80 | 1 |
| Screen_Ratio | CLOB | 20 | 1 |
| Roto_CEL_Product_ID | CLOB | 20 | 1 |
| FX_PricePerM_1 | REAL | 7 | 1 |
| FX_PricePerM_2 | REAL | 7 | 1 |
| FX_PricePerM_3 | REAL | 7 | 1 |
| FX_PricePerM_4 | REAL | 7 | 1 |
| FX_PricePerM_5 | REAL | 7 | 1 |
| FX_PricePerM_6 | REAL | 7 | 1 |
| FX_MiscCharge | REAL | 7 | 1 |
| Currency_Rate_ID | INT32 | 11 | 1 |
| RollUnit_Local | CLOB | 0 | 1 |
| FX_PlateChange_Charge | REAL | 7 | 1 |
| FX_ColorChange_Charge | REAL | 7 | 1 |
| PriceMode_Local | CLOB | 20 | 1 |
| CommissionSource_Local | CLOB | 0 | 1 |
| HP_Indigo_Press_Is_EPM | BOOLEAN | 5 | 1 |
| HP_Indigo_Equip_Is_EPM | BOOLEAN | 5 | 1 |
| HP_Indigo_Equip3_Is_EPM | BOOLEAN | 5 | 1 |
| HP_Indigo_Equip4_Is_EPM | BOOLEAN | 5 | 1 |
| MiscChargeDesc1 | CLOB | 0 | 1 |
| MiscChargeDesc2 | CLOB | 0 | 1 |
| MiscChargeDesc3 | CLOB | 0 | 1 |
| MiscChargeDesc4 | CLOB | 0 | 1 |
| MiscCharge1 | REAL | 7 | 1 |
| MiscCharge2 | REAL | 7 | 1 |
| MiscCharge3 | REAL | 7 | 1 |
| MiscCharge4 | REAL | 7 | 1 |
| FX_MiscCharge1 | REAL | 7 | 1 |
| FX_MiscCharge2 | REAL | 7 | 1 |
| FX_MiscCharge3 | REAL | 7 | 1 |
| FX_MiscCharge4 | REAL | 7 | 1 |
| Frames_Lead_In | INT32 | 11 | 1 |
| Frames_Lead_Out | INT32 | 11 | 1 |
| JobType_Local | CLOB | 10 | 1 |
| PK_UUID | UUID | 0 | 1 |
| NoAcross_OverRide | BOOLEAN | 5 | 1 |
| NoAround_OverRide | BOOLEAN | 5 | 1 |
| Quantity7 | INT32 | 11 | 1 |
| Quantity8 | INT32 | 11 | 1 |
| Quantity9 | INT32 | 11 | 1 |
| Quantity10 | INT32 | 11 | 1 |
| Quantity11 | INT32 | 11 | 1 |
| Quantity12 | INT32 | 11 | 1 |
| Quantity13 | INT32 | 11 | 1 |
| Quantity14 | INT32 | 11 | 1 |
| Quantity15 | INT32 | 11 | 1 |
| Quantity16 | INT32 | 11 | 1 |
| Quantity17 | INT32 | 11 | 1 |
| Quantity18 | INT32 | 11 | 1 |
| PricePerM7 | REAL | 7 | 1 |
| PricePerM8 | REAL | 7 | 1 |
| PricePerM9 | REAL | 7 | 1 |
| PricePerM10 | REAL | 7 | 1 |
| PricePerM11 | REAL | 7 | 1 |
| PricePerM12 | REAL | 7 | 1 |
| PricePerM13 | REAL | 7 | 1 |
| PricePerM14 | REAL | 7 | 1 |
| PricePerM15 | REAL | 7 | 1 |
| PricePerM16 | REAL | 7 | 1 |
| PricePerM17 | REAL | 7 | 1 |
| PricePerM18 | REAL | 7 | 1 |
| FX_PricePerM_7 | REAL | 7 | 1 |
| FX_PricePerM_8 | REAL | 7 | 1 |
| FX_PricePerM_9 | REAL | 7 | 1 |
| FX_PricePerM_10 | REAL | 7 | 1 |
| FX_PricePerM_11 | REAL | 7 | 1 |
| FX_PricePerM_12 | REAL | 7 | 1 |
| FX_PricePerM_13 | REAL | 7 | 1 |
| FX_PricePerM_14 | REAL | 7 | 1 |
| FX_PricePerM_15 | REAL | 7 | 1 |
| FX_PricePerM_16 | REAL | 7 | 1 |
| FX_PricePerM_17 | REAL | 7 | 1 |
| FX_PricePerM_18 | REAL | 7 | 1 |
| PB2_EstimateNum | CLOB | 10 | 1 |
| PB3_EstimateNum | CLOB | 10 | 1 |
| IsPrintReversed | BOOLEAN | 5 | 1 |
| FlexPack_Height | REAL | 7 | 1 |
| FlexPack_Gusset | REAL | 7 | 1 |
| FlexPack_LeftTrim | REAL | 7 | 1 |
| FlexPack_RightTrim | REAL | 7 | 1 |
| Weight1 | REAL | 7 | 1 |
| Weight2 | REAL | 7 | 1 |
| Weight3 | REAL | 7 | 1 |
| Weight4 | REAL | 7 | 1 |
| Weight5 | REAL | 7 | 1 |
| Weight6 | REAL | 7 | 1 |
| FlexPack_Type | INT32 | 11 | 1 |
| Weight7 | REAL | 7 | 1 |
| Weight8 | REAL | 7 | 1 |
| Weight9 | REAL | 7 | 1 |
| Weight10 | REAL | 7 | 1 |
| Weight11 | REAL | 7 | 1 |
| Weight12 | REAL | 7 | 1 |
| Weight13 | REAL | 7 | 1 |
| Weight14 | REAL | 7 | 1 |
| Weight15 | REAL | 7 | 1 |
| Weight16 | REAL | 7 | 1 |
| Weight17 | REAL | 7 | 1 |
| Weight18 | REAL | 7 | 1 |
| FPUD_Popup1 | CLOB | 40 | 1 |
| FPUD_Popup2 | CLOB | 40 | 1 |
| FPUD_Popup3 | CLOB | 40 | 1 |
| FPUD_Popup4 | CLOB | 40 | 1 |
| FPUD_Popup5 | CLOB | 40 | 1 |
| FPUD_Popup6 | CLOB | 40 | 1 |
| StockProduct_ID | CLOB | 10 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |
| Tag | CLOB | 3 | 1 |
| Equip5_ID | CLOB | 10 | 1 |
| Equip5_NoAcross | INT32 | 11 | 1 |
| Equip5_NoAround | INT32 | 11 | 1 |
| Equip5_NoFloods | INT32 | 11 | 1 |
| Equip5_Null_Cycles | INT32 | 11 | 1 |
| Equip5_NumUp_Multiplier | INT32 | 11 | 1 |
| HP_Indigo_Equip5_Is_EPM | BOOLEAN | 5 | 1 |
| Equip5_NoColors | INT16 | 6 | 1 |
| Equip6_ID | CLOB | 10 | 1 |
| Equip6_NoColors | INT32 | 11 | 1 |
| Equip6_NoAcross | INT32 | 11 | 1 |
| Equip6_NoAround | INT32 | 11 | 1 |
| Equip6_Null_Cycles | INT32 | 11 | 1 |
| Equip6_NumUp_Multiplier | INT32 | 11 | 1 |
| HP_Indigo_Equip6_Is_EPM | BOOLEAN | 5 | 1 |
| Equip6_NoFloods | INT32 | 11 | 1 |
| Press_Varnish | CLOB | 40 | 1 |
| Equip_Varnish | CLOB | 40 | 1 |
| Equip3_Varnish | CLOB | 40 | 1 |
| Equip4_Varnish | CLOB | 40 | 1 |
| Equip5_Varnish | CLOB | 40 | 1 |
| Equip6_Varnish | CLOB | 40 | 1 |
| Equip_ColorDescr | CLOB | 80 | 1 |
| Equip3_ColorDescr | CLOB | 80 | 1 |
| Equip4_ColorDescr | CLOB | 80 | 1 |
| Equip5_ColorDescr | CLOB | 80 | 1 |
| Equip6_ColorDescr | CLOB | 80 | 1 |
| Equip_InkType | CLOB | 10 | 1 |
| Equip3_InkType | CLOB | 10 | 1 |
| Equip4_InkType | CLOB | 10 | 1 |
| Equip5_InkType | CLOB | 10 | 1 |
| Equip6_InkType | CLOB | 10 | 1 |
| Tool_NumberAround_Eq2 | INT16 | 6 | 1 |
| Tool_NumberAround_Eq3 | INT16 | 6 | 1 |
| Tool_NumberAround_Eq4 | INT16 | 6 | 1 |
| Tool_NumberAround_Eq5 | INT16 | 6 | 1 |
| Tool_NumberAround_Eq6 | INT16 | 6 | 1 |

### ProductColor

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| UniqueProdID | CLOB | 10 | 1 |
| Unit | INT32 | 11 | 1 |
| Color | CLOB | 40 | 1 |
| Anilox | CLOB | 20 | 1 |
| Ink_Type | CLOB | 20 | 1 |
| Notes | CLOB | 80 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |
| EquipSlot | CLOB | 20 | 1 |

### Product_BillOfMaterials

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| UniqueProdID | CLOB | 10 | 1 |
| Inventory_ID | CLOB | 10 | 1 |
| Part_Number | CLOB | 40 | 1 |
| Quantity_Part | REAL | 7 | 1 |
| Quantity_Label | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### Product_GL_Distribution

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| UniqueProdID | CLOB | 10 | 1 |
| StockProduct_ID | CLOB | 10 | 1 |
| Account_Number | CLOB | 13 | 1 |
| Account_Name | CLOB | 40 | 1 |
| Percent_Applied | REAL | 7 | 1 |
| SP_Inventory_Location | CLOB | 40 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### Product_Inventory

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| StockProduct_ID | CLOB | 10 | 1 |
| Sync_Parent | BOOLEAN | 5 | 1 |
| Qty_Physical | INT32 | 11 | 1 |
| Qty_Allocated | INT32 | 11 | 1 |
| Qty_Available | INT32 | 11 | 1 |
| Qty_BackOrder | INT32 | 11 | 1 |
| u1 | CLOB | 0 | 1 |
| u2 | CLOB | 0 | 1 |
| u3 | CLOB | 0 | 1 |
| u4 | CLOB | 0 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### Product_PostPress

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| UniqueProdID | CLOB | 10 | 1 |
| Equip_Number | CLOB | 10 | 1 |
| Equip_Desc | CLOB | 80 | 1 |
| u1 | CLOB | 0 | 1 |
| Weight_Piece | REAL | 7 | 1 |
| Operations_Desc | CLOB | 40 | 1 |
| PiecesOperation | INT32 | 11 | 1 |
| Operations_Hour | INT32 | 11 | 1 |
| Materials_Desc | CLOB | 40 | 1 |
| Materials_Rate | REAL | 7 | 1 |
| Materials_Unit | CLOB | 15 | 1 |
| Notes | CLOB | 0 | 1 |
| Option_Desc1 | CLOB | 30 | 1 |
| Option_Desc2 | CLOB | 30 | 1 |
| Option_Desc3 | CLOB | 30 | 1 |
| Option_Desc4 | CLOB | 30 | 1 |
| Option_Desc5 | CLOB | 30 | 1 |
| Option_Desc6 | CLOB | 30 | 1 |
| Option_Hours1 | REAL | 7 | 1 |
| Option_Hours2 | REAL | 7 | 1 |
| Option_Hours3 | REAL | 7 | 1 |
| Option_Hours4 | REAL | 7 | 1 |
| Option_Hours5 | REAL | 7 | 1 |
| Option_Hours6 | REAL | 7 | 1 |
| Option_Qty1 | INT32 | 11 | 1 |
| Option_Qty2 | INT32 | 11 | 1 |
| Option_Qty3 | INT32 | 11 | 1 |
| Option_Qty4 | INT32 | 11 | 1 |
| Option_Qty5 | INT32 | 11 | 1 |
| Option_Qty6 | INT32 | 11 | 1 |
| Option_Max1 | INT32 | 11 | 1 |
| Option_Max2 | INT32 | 11 | 1 |
| Option_Max3 | INT32 | 11 | 1 |
| Option_Max4 | INT32 | 11 | 1 |
| Option_Max5 | INT32 | 11 | 1 |
| Option_Max6 | INT32 | 11 | 1 |
| u3 | CLOB | 0 | 1 |
| u4 | CLOB | 0 | 1 |
| u5 | CLOB | 0 | 1 |
| u6 | CLOB | 0 | 1 |
| u7 | CLOB | 0 | 1 |
| u8 | CLOB | 0 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### Product_Tools

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| UniqueProductID | CLOB | 10 | 1 |
| RoutingNo | INT16 | 6 | 1 |
| ToolNo | CLOB | 15 | 1 |
| ToolDescr | CLOB | 15 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### ProfitAdjust

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| Label | CLOB | 20 | 1 |
| MaterialMU | REAL | 7 | 1 |
| LaborMU | REAL | 7 | 1 |
| Commission | REAL | 7 | 1 |
| Reciprocal | BOOLEAN | 5 | 1 |
| EstCost_1 | REAL | 7 | 1 |
| EstCost_2 | REAL | 7 | 1 |
| LaborMU_2 | REAL | 7 | 1 |
| MaterialMU_2 | REAL | 7 | 1 |
| EstCost_3 | REAL | 7 | 1 |
| LaborMU_3 | REAL | 7 | 1 |
| MaterialMU_3 | REAL | 7 | 1 |
| EstCost_4 | REAL | 7 | 1 |
| LaborMU_4 | REAL | 7 | 1 |
| MaterialMU_4 | REAL | 7 | 1 |
| EstCost_5 | REAL | 7 | 1 |
| LaborMU_5 | REAL | 7 | 1 |
| MaterialMU_5 | REAL | 7 | 1 |
| EstCost_6 | REAL | 7 | 1 |
| LaborMU_6 | REAL | 7 | 1 |
| MaterialMU_6 | REAL | 7 | 1 |
| EstCost_7 | REAL | 7 | 1 |
| LaborMU_7 | REAL | 7 | 1 |
| MaterialMU_7 | REAL | 7 | 1 |
| EstCost_8 | REAL | 7 | 1 |
| LaborMU_8 | REAL | 7 | 1 |
| MaterialMU_8 | REAL | 7 | 1 |
| Interpolate | BOOLEAN | 5 | 1 |
| PK_UUID | UUID | 0 | 1 |

### Project_Affiliate

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| Project_Control_ID | INT32 | 11 | 1 |
| Affiliate_Name | CLOB | 40 | 1 |
| From_Date | TIMESTAMP | 19 | 1 |
| To_Date | TIMESTAMP | 19 | 1 |
| Affiliate_ID | INT32 | 11 | 1 |
| Column_Number | INT32 | 11 | 1 |
| Upload_Control_ID | INT32 | 11 | 1 |
| NI_ForBalanceSheet | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |

### Project_Control

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| ProjectName | CLOB | 40 | 1 |
| ScreenWidth | INT32 | 11 | 1 |
| ScreenHeight | INT32 | 11 | 1 |
| FromDate | TIMESTAMP | 19 | 1 |
| ToDate | TIMESTAMP | 19 | 1 |
| PK_UUID | UUID | 0 | 1 |
| Created_Date | TIMESTAMP | 19 | 1 |
| Created_Time | INTERVAL | 10 | 1 |
| Created_Employee_ID | CLOB | 10 | 1 |
| Created_Employee_Name | CLOB | 50 | 1 |
| Modified_Date | TIMESTAMP | 19 | 1 |
| Modified_Time | INTERVAL | 10 | 1 |
| Modified_Employee_ID | CLOB | 255 | 1 |
| Modified_Employee_Name | CLOB | 50 | 1 |

### Project_Data

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| Project_Control_ID | INT32 | 11 | 1 |
| Affiliate_ID | INT32 | 11 | 1 |
| AccountNumber | CLOB | 13 | 1 |
| AccountName | CLOB | 40 | 1 |
| FS_Class | CLOB | 40 | 1 |
| AcctType_Abbr | CLOB | 2 | 1 |
| u1 | CLOB | 0 | 1 |
| Balance_1 | REAL | 7 | 1 |
| u2 | CLOB | 0 | 1 |
| Balance_2 | REAL | 7 | 1 |
| u3 | CLOB | 0 | 1 |
| Balance_3 | REAL | 7 | 1 |
| u4 | CLOB | 0 | 1 |
| Balance_4 | REAL | 7 | 1 |
| u5 | CLOB | 0 | 1 |
| Balance_5 | REAL | 7 | 1 |
| u6 | CLOB | 0 | 1 |
| Balance_6 | REAL | 7 | 1 |
| u7 | CLOB | 0 | 1 |
| Balance_7 | REAL | 7 | 1 |
| u8 | CLOB | 0 | 1 |
| Balance_8 | REAL | 7 | 1 |
| u9 | CLOB | 0 | 1 |
| Balance_9 | REAL | 7 | 1 |
| u10 | CLOB | 0 | 1 |
| Balance_10 | REAL | 7 | 1 |
| Eliminations | REAL | 7 | 1 |
| Combined_Total | REAL | 7 | 1 |
| Project_Affiliate_ID | INT32 | 11 | 1 |
| PLP_BlankRow | CLOB | 2 | 1 |
| u11 | CLOB | 0 | 1 |
| PK_UUID | UUID | 0 | 1 |

### PurchaseOrder

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| PONumber | CLOB | 10 | 1 |
| TicketNum | CLOB | 12 | 1 |
| PODate | TIMESTAMP | 19 | 1 |
| DateReq | TIMESTAMP | 19 | 1 |
| Received | TIMESTAMP | 19 | 1 |
| Description | CLOB | 50 | 1 |
| SizeAcross | REAL | 7 | 1 |
| SizeAround | REAL | 7 | 1 |
| ColSpace | REAL | 7 | 1 |
| RowSpace | REAL | 7 | 1 |
| LabelRepeat | REAL | 7 | 1 |
| NumAcross | INT16 | 6 | 1 |
| NumArounPlate | INT16 | 6 | 1 |
| NumberArounDie | INT16 | 6 | 1 |
| SupplierNum | CLOB | 10 | 1 |
| Signer_AssocNum | CLOB | 10 | 1 |
| Shape | CLOB | 40 | 1 |
| Patched_ShipToAddress | TIMESTAMP | 19 | 1 |
| DieCut | INT16 | 6 | 1 |
| OrderStockNum | CLOB | 10 | 1 |
| MFGSpec | CLOB | 30 | 1 |
| Steel | CLOB | 15 | 1 |
| CornerRadius | REAL | 7 | 1 |
| ChromePlate | BOOLEAN | 5 | 1 |
| Quantity | INT16 | 6 | 1 |
| AutoAppl | BOOLEAN | 5 | 1 |
| FinalUnwind | CLOB | 15 | 1 |
| TopCoat | CLOB | 30 | 1 |
| ThroughInk | BOOLEAN | 5 | 1 |
| EquipNum | CLOB | 10 | 1 |
| StockNo1 | CLOB | 10 | 1 |
| StockNo2 | CLOB | 10 | 1 |
| StockNo3 | CLOB | 10 | 1 |
| WebWidth | REAL | 7 | 1 |
| ShipVia | CLOB | 40 | 1 |
| QCOType | CLOB | 12 | 1 |
| POType | CLOB | 20 | 1 |
| MasterWidth | REAL | 7 | 1 |
| ToolNum | CLOB | 15 | 1 |
| FaceColor | CLOB | 15 | 1 |
| FaceCaliper | CLOB | 15 | 1 |
| Adhesive | CLOB | 20 | 1 |
| CostMSI | REAL | 7 | 1 |
| Items_subtable | INT32 | 11 | 1 |
| Notes | CLOB | 0 | 1 |
| TotalPO | REAL | 7 | 1 |
| LinerCaliper | CLOB | 15 | 1 |
| FaceStock | CLOB | 80 | 1 |
| SellPrice | REAL | 7 | 1 |
| Supplier | CLOB | 80 | 1 |
| Invoiced | BOOLEAN | 5 | 1 |
| InvoiceNum | CLOB | 10 | 1 |
| Closed | BOOLEAN | 5 | 1 |
| Press | CLOB | 10 | 1 |
| ToolWidth | REAL | 7 | 1 |
| Signer_AssocName | CLOB | 40 | 1 |
| LamStock | CLOB | 80 | 1 |
| ActShipDate | TIMESTAMP | 19 | 1 |
| PhoneNo | CLOB | 20 | 1 |
| ProofNeed | CLOB | 60 | 1 |
| EntryDate | TIMESTAMP | 19 | 1 |
| EntryBy | CLOB | 50 | 1 |
| ModifyDate | TIMESTAMP | 19 | 1 |
| ModifyBy | CLOB | 50 | 1 |
| A4LinkDate | TIMESTAMP | 19 | 1 |
| SendToA4 | CLOB | 20 | 1 |
| A4VoucherID | INT32 | 11 | 1 |
| A4LinkBatchID | INT32 | 11 | 1 |
| ShipCountry | CLOB | 25 | 1 |
| Ship_Address_ID | CLOB | 10 | 1 |
| DontVoucher | BOOLEAN | 5 | 1 |
| ShipName | CLOB | 80 | 1 |
| ShipAddr1 | CLOB | 255 | 1 |
| ShipAddr2 | CLOB | 255 | 1 |
| ShipCity | CLOB | 40 | 1 |
| ShipState | CLOB | 25 | 1 |
| ShipZip | CLOB | 15 | 1 |
| ShipAttention | CLOB | 40 | 1 |
| Account_No | CLOB | 30 | 1 |
| VndAttention | CLOB | 40 | 1 |
| TimeDue | CLOB | 10 | 1 |
| Status | CLOB | 20 | 1 |
| Return_PO_ID | CLOB | 10 | 1 |
| Terms | CLOB | 45 | 1 |
| FOB | CLOB | 30 | 1 |
| PO_Subtotal | REAL | 7 | 1 |
| Tax | REAL | 7 | 1 |
| Freight | REAL | 7 | 1 |
| ToolPOSource | CLOB | 12 | 1 |
| PushPO_ToAP_Status | CLOB | 20 | 1 |
| AP_Invoice_ID | INT32 | 11 | 1 |
| Received_Total | REAL | 7 | 1 |
| RequestedDeliveryDate | TIMESTAMP | 19 | 1 |
| eCommerceSendPOstatus | CLOB | 20 | 1 |
| TaxCB_TaxPO_i | INT32 | 11 | 1 |
| EntryTime | INTERVAL | 10 | 1 |
| ModifyTime | INTERVAL | 10 | 1 |
| OverrideStockPricing | BOOLEAN | 5 | 1 |
| TaxRegionID | INT32 | 11 | 1 |
| TaxRegionRate | REAL | 7 | 1 |
| Received_Tax | REAL | 7 | 1 |
| DieBlank | BOOLEAN | 5 | 1 |
| FC_Supplier_Currency_ID | INT32 | 11 | 1 |
| FC_Supplier_ExchangeRate | REAL | 7 | 1 |
| FC_Supplier_UnitPrice | REAL | 7 | 1 |
| Yield_Area_Weight | REAL | 7 | 1 |
| FC_Supplier_Currency_Rate_ID | INT32 | 11 | 1 |
| Price_Weight | REAL | 7 | 1 |
| Inventory_Location | CLOB | 40 | 1 |
| Roto_UOM_Code | CLOB | 20 | 1 |
| Roto_ProdFam_Code | CLOB | 20 | 1 |
| Roto_CavityShape_Code | CLOB | 20 | 1 |
| Roto_LayoutOpt_Code | CLOB | 20 | 1 |
| Roto_CutType_Code | CLOB | 20 | 1 |
| Roto_CutPosition_Code | CLOB | 20 | 1 |
| Roto_LabelAppl_Code | CLOB | 20 | 1 |
| Roto_Treatment_Code | CLOB | 20 | 1 |
| Roto_DrillShaft_Code | CLOB | 20 | 1 |
| Roto_BladeHeight_Code | CLOB | 20 | 1 |
| Roto_NonStickText | CLOB | 20 | 1 |
| Roto_NumHolesPerCavity | CLOB | 20 | 1 |
| Roto_PatternCentered | CLOB | 20 | 1 |
| Roto_Quote_Number | CLOB | 80 | 1 |
| Roto_Quote_Line_ID | CLOB | 80 | 1 |
| Roto_Quote_Status | CLOB | 80 | 1 |
| Roto_SpecialBladeHeight | CLOB | 20 | 1 |
| Roto_Num_Perf_Sets | CLOB | 20 | 1 |
| BillTo_AddressID | CLOB | 20 | 1 |
| BillTo_Name | CLOB | 80 | 1 |
| BillTo_Addr1 | CLOB | 255 | 1 |
| BillTo_Addr2 | CLOB | 255 | 1 |
| BillTo_City | CLOB | 40 | 1 |
| BillTo_State | CLOB | 25 | 1 |
| BillTo_Zip | CLOB | 15 | 1 |
| BillTo_Country | CLOB | 25 | 1 |
| BillTo_Attention | CLOB | 40 | 1 |
| Roto_CEL_Product_ID | CLOB | 20 | 1 |
| Tool_NumberAround | INT32 | 11 | 1 |
| ShipeCommShipToID | CLOB | 25 | 1 |
| DieCut_Local | CLOB | 0 | 1 |
| FC_Customer_Currency_ID | INT32 | 11 | 1 |
| FC_Customer_Currency_Rate_ID | INT32 | 11 | 1 |
| FC_Customer_ExchangeRate | REAL | 7 | 1 |
| FC_Customer_SellPrice | REAL | 7 | 1 |
| Roto_DieUse_Code | CLOB | 0 | 1 |
| Roto_Laser_Harden | BOOLEAN | 5 | 1 |
| Roto_Plate_Length | REAL | 7 | 1 |
| Roto_Plate_Width | REAL | 7 | 1 |
| Roto_SetPageAndPop | CLOB | 0 | 1 |
| Roto_Plate_Height | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |
| Flexo_HotS | CLOB | 30 | 1 |
| OnSaved_TXT | CLOB | 0 | 1 |
| POType_Local | CLOB | 0 | 1 |
| QCOType_Local | CLOB | 0 | 1 |
| Core_Size | REAL | 7 | 1 |
| FC_PO_Subtotal | REAL | 7 | 1 |
| FC_Tax | REAL | 7 | 1 |
| FC_Received_Total | REAL | 7 | 1 |
| FC_Received_Tax | REAL | 7 | 1 |
| FC_Price_Weight | REAL | 7 | 1 |
| FlexPack_Height | REAL | 7 | 1 |
| FlexPack_Gusset | REAL | 7 | 1 |
| FlexPack_LeftTrim | REAL | 7 | 1 |
| FlexPack_RightTrim | REAL | 7 | 1 |
| FC_Freight | REAL | 7 | 1 |
| FC_TotalPO | REAL | 7 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |
| Tag | CLOB | 255 | 1 |

### PurchaseOrder_Items

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| Quantity | REAL | 7 | 1 |
| Description | CLOB | 80 | 1 |
| UnitPrice | REAL | 7 | 1 |
| Amount | REAL | 7 | 1 |
| OrderFootage | INT32 | 11 | 1 |
| ReceiveFootage | INT32 | 11 | 1 |
| RollNum | INT16 | 6 | 1 |
| Cut1 | REAL | 7 | 1 |
| Cut2 | REAL | 7 | 1 |
| Cut3 | REAL | 7 | 1 |
| Cut4 | REAL | 7 | 1 |
| Cut5 | REAL | 7 | 1 |
| NumCut1 | INT16 | 6 | 1 |
| NumCut2 | INT16 | 6 | 1 |
| NumCut3 | INT16 | 6 | 1 |
| NumCut4 | INT16 | 6 | 1 |
| NumCut5 | INT16 | 6 | 1 |
| RollOffCut | REAL | 7 | 1 |
| EntryDate | TIMESTAMP | 19 | 1 |
| EntryBy | CLOB | 35 | 1 |
| ModifyDate | TIMESTAMP | 19 | 1 |
| ModifyBy | CLOB | 30 | 1 |
| A4LinkDate | TIMESTAMP | 19 | 1 |
| SendToA4 | CLOB | 20 | 1 |
| A4VoucherID | INT32 | 11 | 1 |
| A4VendorID | INT32 | 11 | 1 |
| A4LinkBatchID | INT32 | 11 | 1 |
| ReceiptBatchID | INT32 | 11 | 1 |
| ReceiveDate | TIMESTAMP | 19 | 1 |
| ReceiptBatchStatus | CLOB | 20 | 1 |
| PushPORecToAP_Status | CLOB | 20 | 1 |
| AP_Invoice_ID | INT32 | 11 | 1 |
| FassonOnOrder | CLOB | 10 | 1 |
| ExactWidths | BOOLEAN | 5 | 1 |
| EntryTime | INTERVAL | 10 | 1 |
| ModifyTime | INTERVAL | 10 | 1 |
| id_added_by_converter | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |

### QP_Event

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| QP_ID | INT32 | 11 | 1 |
| Event_Key | CLOB | 30 | 1 |
| Is_InUseState | BOOLEAN | 5 | 1 |
| Event_Title | CLOB | 30 | 1 |
| PK_UUID | UUID | 0 | 1 |

### Quality_Log

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| User_Type | CLOB | 40 | 1 |
| Invoice_ID | CLOB | 10 | 1 |
| Ticket_ID | CLOB | 10 | 1 |
| Customer_ID | CLOB | 10 | 1 |
| Customer_Name | CLOB | 80 | 1 |
| Materials_Received | BOOLEAN | 5 | 1 |
| Received | TIMESTAMP | 19 | 1 |
| Received_by_Employee_ID | CLOB | 10 | 1 |
| Received_by_Employee_Name | CLOB | 60 | 1 |
| User_Reviewed | BOOLEAN | 5 | 1 |
| Reviewed | TIMESTAMP | 19 | 1 |
| Reviewed_by_Employee_ID | CLOB | 10 | 1 |
| Reviewed_by_Employee_Name | CLOB | 60 | 1 |
| Record_Type | CLOB | 30 | 1 |
| Description | CLOB | 80 | 1 |
| Modified_Date | TIMESTAMP | 19 | 1 |
| Modified_Time | INTERVAL | 10 | 1 |
| Modified_by_Employee_ID | CLOB | 10 | 1 |
| Modified_by_Employee_Name | CLOB | 60 | 1 |
| Detailed_Explaination | CLOB | 0 | 1 |
| Notes | CLOB | 0 | 1 |
| Corrective_Action | CLOB | 0 | 1 |
| Contact_ID | CLOB | 10 | 1 |
| Contact_Name | CLOB | 41 | 1 |
| Contact_Phone | CLOB | 15 | 1 |
| Contact_Extension | CLOB | 5 | 1 |
| User_Issued | BOOLEAN | 5 | 1 |
| Issued | TIMESTAMP | 19 | 1 |
| Issued_by_Employee_ID | CLOB | 10 | 1 |
| Issued_by_Employee_Name | CLOB | 60 | 1 |
| Created_Date | TIMESTAMP | 19 | 1 |
| Created_Time | INTERVAL | 10 | 1 |
| Created_by_Employee_ID | CLOB | 10 | 1 |
| Created_by_Employee_Name | CLOB | 60 | 1 |
| Total_Cost | REAL | 7 | 1 |
| Material_Cost | REAL | 7 | 1 |
| Freight_Cost | REAL | 7 | 1 |
| Credit_Amount | REAL | 7 | 1 |
| Check_Number | CLOB | 20 | 1 |
| Vendor_ID | CLOB | 10 | 1 |
| Vendor_Name | CLOB | 80 | 1 |
| StockNumber | CLOB | 10 | 1 |
| InventoryNumber | CLOB | 10 | 1 |
| MiscCostDescr | CLOB | 20 | 1 |
| MiscCostAmount | REAL | 7 | 1 |
| Inventory_PartNumber | CLOB | 40 | 1 |
| PO_Number | CLOB | 30 | 1 |
| EndUser_ID | CLOB | 10 | 1 |
| EndUser_Name | CLOB | 80 | 1 |
| Replacement_Ticket_ID | CLOB | 10 | 1 |
| CustomProduct_PartNumber | CLOB | 30 | 1 |
| CustomProduct_Description | CLOB | 80 | 1 |
| StockProduct_PartNumber | CLOB | 30 | 1 |
| StockProduct_Description | CLOB | 0 | 1 |
| Is_Closed | BOOLEAN | 5 | 1 |
| Closed_Date | TIMESTAMP | 19 | 1 |
| Closed_by_Employee_ID | CLOB | 10 | 1 |
| Closed_by_Employee_Name | CLOB | 60 | 1 |
| Is_Credit_Issued | BOOLEAN | 5 | 1 |
| Credit_Issued_Date | TIMESTAMP | 19 | 1 |
| Credit_Issued_by_Employee_ID | CLOB | 10 | 1 |
| Credit_Issued_by_Employee_Name | CLOB | 60 | 1 |
| Is_Action_Taken | BOOLEAN | 5 | 1 |
| Action_Date | TIMESTAMP | 19 | 1 |
| Action_Taken_by_Employee_ID | CLOB | 10 | 1 |
| Action_Taken_by_Employee_Name | CLOB | 60 | 1 |
| Severity | CLOB | 40 | 1 |
| ActionType | CLOB | 40 | 1 |
| Root_Cause | CLOB | 0 | 1 |
| Verification | CLOB | 0 | 1 |
| Due_Date | TIMESTAMP | 19 | 1 |
| Effective | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |
| Tag | CLOB | 3 | 1 |

### Quality_Procedure

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| QP_Type | CLOB | 30 | 1 |
| QP_Priority | CLOB | 30 | 1 |
| Description | CLOB | 80 | 1 |
| Color_in_List | CLOB | 30 | 1 |
| List_in_All_Areas | BOOLEAN | 5 | 1 |
| Created_Date | TIMESTAMP | 19 | 1 |
| Created_Time | INTERVAL | 10 | 1 |
| Created_Employee_ID | CLOB | 10 | 1 |
| Created_Employee_Name | CLOB | 50 | 1 |
| Modified_Date | TIMESTAMP | 19 | 1 |
| Modified_Time | INTERVAL | 10 | 1 |
| Modified_Employee_ID | CLOB | 10 | 1 |
| Modified_Employee_Name | CLOB | 50 | 1 |
| Customer_ID | CLOB | 10 | 1 |
| Customer_Name | CLOB | 80 | 1 |
| Product_ID | CLOB | 30 | 1 |
| Product_PartNumber | CLOB | 40 | 1 |
| Product_JobName | CLOB | 80 | 1 |
| Revision | CLOB | 40 | 1 |
| Status | CLOB | 30 | 1 |
| InActive | BOOLEAN | 5 | 1 |
| Rule_Type | CLOB | 30 | 1 |
| EndUser_ID | CLOB | 10 | 1 |
| EndUser_Name | CLOB | 80 | 1 |
| Tool_Number | CLOB | 15 | 1 |
| Tool_Description | CLOB | 20 | 1 |
| Stock_Number | CLOB | 10 | 1 |
| Stock_Description | CLOB | 40 | 1 |
| Product_Group_ID | CLOB | 40 | 1 |
| Inventory_PartNumber | CLOB | 40 | 1 |
| Inventory_Description | CLOB | 80 | 1 |
| Inventory_VendorPartNo | CLOB | 40 | 1 |
| Supplier_Number | CLOB | 10 | 1 |
| Supplier_Company | CLOB | 50 | 1 |
| SP_Product_ID | CLOB | 10 | 1 |
| SP_Product_Number | CLOB | 30 | 1 |
| SP_Description | CLOB | 80 | 1 |
| SP_Group | CLOB | 20 | 1 |
| SP_Type | CLOB | 35 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 255 | 1 |
| Tag | CLOB | 3 | 1 |
| Equipment_Number | CLOB | 10 | 1 |
| Equipment_Description | CLOB | 35 | 1 |

### Reports

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ReportName | CLOB | 60 | 1 |
| Description | CLOB | 0 | 1 |
| Format | BLOB | 0 | 1 |
| AssocFile | INT32 | 11 | 1 |
| Email_Format | CLOB | 20 | 1 |
| QuickReport | BLOB | 0 | 1 |
| ReportType | CLOB | 20 | 1 |
| DisplayInMenu | BOOLEAN | 5 | 1 |
| PDF_Name | CLOB | 30 | 1 |
| Is_Email_PDF | BOOLEAN | 5 | 1 |
| DisplayInMenu_TimeCard | BOOLEAN | 5 | 1 |
| Is_PDF_Append_ReferenceInfo | BOOLEAN | 5 | 1 |
| Detail_only | BOOLEAN | 5 | 1 |
| PK_UUID | UUID | 0 | 1 |
| DisplayOrder | INT32 | 11 | 1 |
| Is_User_Default | BOOLEAN | 5 | 1 |
| Is_ThermometerOff | BOOLEAN | 5 | 1 |
| Is_Label | BOOLEAN | 5 | 1 |
| Is_Label_Default | BOOLEAN | 5 | 1 |
| Is_Append_to_Subject | BOOLEAN | 5 | 1 |
| Is_previewInMenu | BOOLEAN | 5 | 1 |
| Is_Label_WIP_Default | BOOLEAN | 5 | 1 |
| Is_Label_Fin_Default | BOOLEAN | 5 | 1 |

### RollStock

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| IDNumber | CLOB | 60 | 1 |
| StockNum | CLOB | 20 | 1 |
| PONumber | CLOB | 20 | 1 |
| AllocTikNum | CLOB | 20 | 1 |
| UsedTikNum | CLOB | 20 | 1 |
| Width | REAL | 7 | 1 |
| FootLength | INT32 | 11 | 1 |
| PrintFlag | BOOLEAN | 5 | 1 |
| Location | CLOB | 60 | 1 |
| Description | CLOB | 0 | 1 |
| Upload1 | BOOLEAN | 5 | 1 |
| Upload2 | BOOLEAN | 5 | 1 |
| DeleteFlag | BOOLEAN | 5 | 1 |
| RollNum | INT16 | 6 | 1 |
| StkDate | TIMESTAMP | 19 | 1 |
| StkUsed | BOOLEAN | 5 | 1 |
| Slitted | BOOLEAN | 5 | 1 |
| SlitFootage | INT32 | 11 | 1 |
| CostMSI | REAL | 7 | 1 |
| CostOfRoll | REAL | 7 | 1 |
| DateRollUsed | TIMESTAMP | 19 | 1 |
| ALT_IDNumber | CLOB | 60 | 1 |
| FassonShipID | INT32 | 11 | 1 |
| CreatedDate | TIMESTAMP | 19 | 1 |
| OpStamp | CLOB | 10 | 1 |
| DateStamp | TIMESTAMP | 19 | 1 |
| Used_TimeStamp | INTERVAL | 10 | 1 |
| Allocated_CB | BOOLEAN | 5 | 1 |
| Coated_By | CLOB | 10 | 1 |
| Coated_Date | TIMESTAMP | 19 | 1 |
| Coated_Time | INTERVAL | 10 | 1 |
| Orig_RollID | CLOB | 60 | 1 |
| Press | CLOB | 10 | 1 |
| PK_UUID | UUID | 0 | 1 |
| Currency_ID | INT32 | 11 | 1 |
| Orig_Curr_ExchangeRate | REAL | 7 | 1 |
| FC_CostMSI | REAL | 7 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |
| Tag | CLOB | 3 | 1 |
| rsStatus | CLOB | 0 | 1 |
| rsStatus_Org | CLOB | 0 | 1 |
| RFID | INT32 | 11 | 1 |
| SlittedFlag | BOOLEAN | 5 | 1 |
| WIP_Location | CLOB | 30 | 1 |
| is_WIP | BOOLEAN | 5 | 1 |
| WIP_CreatedTicketNum | CLOB | 20 | 1 |
| WIP_WorkStatus | BOOLEAN | 5 | 1 |
| WIP_RouteStep | CLOB | 20 | 1 |
| WIP_LaneDesignation | CLOB | 3 | 1 |
| WIP_NoAcross | INT32 | 11 | 1 |
| WIP_Sequence | INT32 | 11 | 1 |
| WIP_NoLabel | INT32 | 11 | 1 |

### RotoMetricsPressIDs

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| EquipmentNumber | CLOB | 10 | 1 |
| CEL_Product_ID | CLOB | 20 | 1 |
| Product_ID_Description | CLOB | 80 | 1 |
| PK_UUID | UUID | 0 | 1 |

### RotoMetrics_LOV_Codes

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| Field_Element | CLOB | 40 | 1 |
| LOV_Meaning | CLOB | 40 | 1 |
| LOV_Code | CLOB | 20 | 1 |
| Inactive | BOOLEAN | 5 | 1 |
| DefaultCode | BOOLEAN | 5 | 1 |
| Tool_Num | CLOB | 0 | 1 |
| PK_UUID | UUID | 0 | 1 |

### SC_Actions

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| Primary_Key | INT32 | 11 | 1 |
| Form | INT32 | 11 | 1 |
| Item | INT32 | 11 | 1 |
| Code | CLOB | 30 | 1 |
| Actions_Order | INT16 | 6 | 1 |
| Disable | BOOLEAN | 5 | 1 |
| Actions_Default | BOOLEAN | 5 | 1 |
| Rule | INT16 | 6 | 1 |
| EQ | BOOLEAN | 5 | 1 |
| PK_UUID | UUID | 0 | 1 |

### SC_Equipment_Downtime

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 0 |
| PK_UUID | UUID | 0 | 1 |
| Name | CLOB | 40 | 1 |
| Shift_Start | INTERVAL | 10 | 1 |
| Shift_End | INTERVAL | 10 | 1 |
| Equipment_ID | INT32 | 11 | 1 |
| Day_of_week | INT16 | 6 | 1 |
| Week_day | CLOB | 3 | 1 |

### SC_Equipment_group

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| Primary_Key | INT32 | 11 | 1 |
| Name | CLOB | 255 | 1 |
| PK_UUID | UUID | 0 | 1 |

### SC_Equipment_group_Items

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| Primary_key | INT32 | 11 | 1 |
| Group_key | INT32 | 11 | 1 |
| Equipment_key | INT32 | 11 | 1 |
| AVL_01 | CLOB | 255 | 1 |
| AVL_02 | CLOB | 255 | 1 |
| AVL_03 | CLOB | 255 | 1 |
| AVL_04 | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |

### SC_Event

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| EVENT_ID | INT32 | 11 | 1 |
| EQUIPMENT_ID | INT32 | 11 | 1 |
| MasterEvent_ID | INT32 | 11 | 1 |
| StartDate | TIMESTAMP | 19 | 1 |
| StartTime | INTERVAL | 10 | 1 |
| EndDate | TIMESTAMP | 19 | 1 |
| EndTime | INTERVAL | 10 | 1 |
| Color | INT32 | 11 | 1 |
| Locked | BOOLEAN | 5 | 1 |
| Event_code | CLOB | 0 | 1 |
| Description | CLOB | 0 | 1 |
| Downtime | BOOLEAN | 5 | 1 |
| Event_Status | CLOB | 20 | 1 |
| Duration | INTERVAL | 10 | 1 |
| New_Event | BOOLEAN | 5 | 1 |
| Done | BOOLEAN | 5 | 1 |
| Operations_key | INT32 | 11 | 1 |
| Order_Sequence | INT16 | 6 | 1 |
| Employee_key | INT32 | 11 | 1 |
| Behind_Schedule | BOOLEAN | 5 | 1 |
| Segment | INT16 | 6 | 1 |
| Auto_Reschedule | BOOLEAN | 5 | 1 |
| Event_Open | BOOLEAN | 5 | 1 |
| Ship_By_Date | TIMESTAMP | 19 | 1 |
| AVL_03 | BOOLEAN | 5 | 1 |
| AVL_04 | BOOLEAN | 5 | 1 |
| AVL_05 | BOOLEAN | 5 | 1 |
| AVL_06 | BOOLEAN | 5 | 1 |
| AVL_07 | BOOLEAN | 5 | 1 |
| AVL_08 | BOOLEAN | 5 | 1 |
| AVL_09 | BOOLEAN | 5 | 1 |
| AVL_10 | BOOLEAN | 5 | 1 |
| AVL_11 | BOOLEAN | 5 | 1 |
| AVL_12 | BOOLEAN | 5 | 1 |
| PK_UUID | UUID | 0 | 1 |

### SC_MasterEvent

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| MasterEvent_ID | INT32 | 11 | 1 |
| Ticket_Number | CLOB | 20 | 1 |
| Ticket_Desc | CLOB | 0 | 1 |
| Ticket_Status | CLOB | 20 | 1 |
| Customer_No | CLOB | 20 | 1 |
| Customer_Name | CLOB | 80 | 1 |
| PO_Number | CLOB | 25 | 1 |
| Ship_By_Date | TIMESTAMP | 19 | 1 |
| Press_Pass_Total | INT32 | 11 | 1 |
| Press_Pass_Position | INT32 | 11 | 1 |
| Press_Equipment | CLOB | 10 | 1 |
| LT_Last_Update_Date | TIMESTAMP | 19 | 1 |
| LT_Last_Update_Time | INTERVAL | 10 | 1 |
| Main_Tool | CLOB | 15 | 1 |
| StockWidth1_Laminate | REAL | 7 | 1 |
| StockNum1_Laminate | CLOB | 10 | 1 |
| StockWidth2_MainStock | REAL | 7 | 1 |
| StockNum2_MainStock | CLOB | 10 | 1 |
| Downtime_Press | CLOB | 10 | 1 |
| Downtime_Hours | REAL | 7 | 1 |
| Press_Hours_Estimate | REAL | 7 | 1 |
| Press_Footage_Estimate | INT32 | 11 | 1 |
| Event_Status | CLOB | 20 | 1 |
| Press_Pass_Abs_Position | INT32 | 11 | 1 |
| ITSName | CLOB | 35 | 1 |
| OTSName | CLOB | 35 | 1 |
| EndUserPO | CLOB | 30 | 1 |
| NoPlateChanges | INT32 | 11 | 1 |
| NoColorChanges | INT32 | 11 | 1 |
| ArtStat | CLOB | 20 | 1 |
| ArtDone | BOOLEAN | 5 | 1 |
| ProofStat | CLOB | 20 | 1 |
| ProofDone | BOOLEAN | 5 | 1 |
| PlateStat | CLOB | 20 | 1 |
| PlateDone | BOOLEAN | 5 | 1 |
| ToolStat | CLOB | 20 | 1 |
| ToolsIn | BOOLEAN | 5 | 1 |
| Ink_Status | CLOB | 20 | 1 |
| Is_Ink_In | BOOLEAN | 5 | 1 |
| StockIn_Local | CLOB | 0 | 1 |
| Stock_Allocated | BOOLEAN | 5 | 1 |
| Code | CLOB | 255 | 1 |
| Schedule | BOOLEAN | 5 | 1 |
| Duration | REAL | 7 | 1 |
| Segments | INT16 | 6 | 1 |
| Gear_Teeth | INT32 | 11 | 1 |
| StockIn | CLOB | 3 | 1 |
| ColorDescr | CLOB | 80 | 1 |
| PK_UUID | UUID | 0 | 1 |
| Priority | CLOB | 31 | 1 |

### SC_Preferences

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| Primary_Key | INT32 | 11 | 1 |
| StartWeekOn | INT32 | 11 | 1 |
| StartDayAt | INTERVAL | 10 | 1 |
| EndDayAt | INTERVAL | 10 | 1 |
| DefaultEventText | CLOB | 80 | 1 |
| Downtime_Color | INT32 | 11 | 1 |
| StartWorkDayAt | INTERVAL | 10 | 1 |
| EndWorkDayAt | INTERVAL | 10 | 1 |
| Resource_downtime_draw | BOOLEAN | 5 | 1 |
| VariableColumnWidth | BOOLEAN | 5 | 1 |
| VariableRowHeight | BOOLEAN | 5 | 1 |
| Mon | BOOLEAN | 5 | 1 |
| Tue | BOOLEAN | 5 | 1 |
| Wed | BOOLEAN | 5 | 1 |
| Thu | BOOLEAN | 5 | 1 |
| Fri | BOOLEAN | 5 | 1 |
| Sat | BOOLEAN | 5 | 1 |
| Sun | BOOLEAN | 5 | 1 |
| New_event_color | INT32 | 11 | 1 |
| Lock_color | INT32 | 11 | 1 |
| Done_color | INT32 | 11 | 1 |
| Current_DateTime_color | INT32 | 11 | 1 |
| Equipment_down_color | INT32 | 11 | 1 |
| Behind_color | INT32 | 11 | 1 |
| Time_Unit | INTERVAL | 10 | 1 |
| Split_color | INT32 | 11 | 1 |
| Auto_Reschedule_color | INT32 | 11 | 1 |
| Promt_1 | BOOLEAN | 5 | 1 |
| Rules_Actions_Order | CLOB | 10 | 1 |
| Day_View | BOOLEAN | 5 | 1 |
| Time_Intervals | INT16 | 6 | 1 |
| Promt_2 | BOOLEAN | 5 | 1 |
| Promt_3 | BOOLEAN | 5 | 1 |
| Promt_4 | BOOLEAN | 5 | 1 |
| Promt_5 | BOOLEAN | 5 | 1 |
| Promt_6 | BOOLEAN | 5 | 1 |
| Promt_7 | BOOLEAN | 5 | 1 |
| Code | CLOB | 255 | 1 |
| Rules_Promt_Sequence | CLOB | 255 | 1 |
| Actions_Code | CLOB | 255 | 1 |
| Event_Fields_Selected | BLOB | 0 | 1 |
| Add_event_Description | BOOLEAN | 5 | 1 |
| Field_DIlemeter | CLOB | 4 | 1 |
| Past_due_color | INT32 | 11 | 1 |
| Due_today_color | INT32 | 11 | 1 |
| Full_day | BOOLEAN | 5 | 1 |
| SHIft_Color | INT32 | 11 | 1 |
| Shift_Changes | BOOLEAN | 5 | 1 |
| Shift_change_defualt | CLOB | 255 | 1 |
| Automatic_Action | CLOB | 10 | 1 |
| Apply_rules | BOOLEAN | 5 | 1 |
| Promt_8 | BOOLEAN | 5 | 1 |
| AVL_24 | BOOLEAN | 5 | 1 |
| AVL_25 | BOOLEAN | 5 | 1 |
| AVL_26 | BOOLEAN | 5 | 1 |
| AVL_27 | BOOLEAN | 5 | 1 |
| AVL_28 | BOOLEAN | 5 | 1 |
| AVL_29 | BOOLEAN | 5 | 1 |
| AVL_30 | BOOLEAN | 5 | 1 |
| AVL_31 | BOOLEAN | 5 | 1 |
| AVL_32 | BOOLEAN | 5 | 1 |
| AVL_33 | BOOLEAN | 5 | 1 |
| AVL_34 | BOOLEAN | 5 | 1 |
| AVL_35 | BOOLEAN | 5 | 1 |
| AVL_36 | BOOLEAN | 5 | 1 |
| AVL_37 | BOOLEAN | 5 | 1 |
| AVL_38 | BOOLEAN | 5 | 1 |
| AVL_39 | BOOLEAN | 5 | 1 |
| AVL_40 | BOOLEAN | 5 | 1 |
| AVL_41 | BOOLEAN | 5 | 1 |
| AVL_42 | BOOLEAN | 5 | 1 |
| AVL_43 | BOOLEAN | 5 | 1 |
| AVL_44 | BOOLEAN | 5 | 1 |
| AVL_45 | BOOLEAN | 5 | 1 |
| AVL_46 | BOOLEAN | 5 | 1 |
| PK_UUID | UUID | 0 | 1 |

### SC_Shifts

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 0 |
| PK_UUID | UUID | 0 | 1 |
| Day_of_week | INT16 | 6 | 1 |
| Name | CLOB | 40 | 1 |
| Shift_Start | INTERVAL | 10 | 1 |
| Shift_End | INTERVAL | 10 | 1 |
| Week_day | CLOB | 3 | 1 |

### SC_Time_Card

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| Primary_key | INT32 | 11 | 1 |
| StartDate | TIMESTAMP | 19 | 1 |
| Start_Tme | INTERVAL | 10 | 1 |
| EndDate | TIMESTAMP | 19 | 1 |
| EndTime | INTERVAL | 10 | 1 |
| Employee_key | INT32 | 11 | 1 |
| Event_key | INT32 | 11 | 1 |
| Resource_key | INT32 | 11 | 1 |
| Operations_key | INT32 | 11 | 1 |
| Note | CLOB | 0 | 1 |
| Elapsed | INTERVAL | 10 | 1 |
| Close_Operation | BOOLEAN | 5 | 1 |
| AVL_01 | BOOLEAN | 5 | 1 |
| AVL_02 | BOOLEAN | 5 | 1 |
| AVL_03 | BOOLEAN | 5 | 1 |
| AVL_04 | BOOLEAN | 5 | 1 |
| AVL_05 | BOOLEAN | 5 | 1 |
| PK_UUID | UUID | 0 | 1 |

### SP_Inventory_Add

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| StockProduct_ID | CLOB | 10 | 1 |
| Entered_Date | TIMESTAMP | 19 | 1 |
| Entered_Time | INTERVAL | 10 | 1 |
| Entered_By | CLOB | 51 | 1 |
| Inventory_Date | TIMESTAMP | 19 | 1 |
| Inventory_Time | INTERVAL | 10 | 1 |
| Inventory_DateTime_Stamp | INT32 | 11 | 1 |
| Expiration_Date | TIMESTAMP | 19 | 1 |
| Inventory_Quantity | INT32 | 11 | 1 |
| Inventory_Balance | INT32 | 11 | 1 |
| Cost_Unit | CLOB | 20 | 1 |
| Item_Cost | REAL | 7 | 1 |
| Location | CLOB | 40 | 1 |
| Custom_Ticket_ID | CLOB | 10 | 1 |
| Custom_Ticket_CustPONum | CLOB | 30 | 1 |
| Source_PONumber | CLOB | 10 | 1 |
| Source_POItems_ID | CLOB | 10 | 1 |
| Source_Product_UniqueProdID | CLOB | 10 | 1 |
| Source_PackSlipItem_ID | CLOB | 10 | 1 |
| Notes | CLOB | 80 | 1 |
| Modified_Date | TIMESTAMP | 19 | 1 |
| Modified_Time | INTERVAL | 10 | 1 |
| Modified_By | CLOB | 51 | 1 |
| Modification_Count | INT32 | 11 | 1 |
| Is_User_Made | BOOLEAN | 5 | 1 |
| Releases_Allowed | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |
| Cost_Unit_Local | CLOB | 20 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |

### SP_Inventory_Release

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| SP_Inventory_Add_ID | CLOB | 10 | 1 |
| StockProduct_ID | CLOB | 10 | 1 |
| Entered_Date | TIMESTAMP | 19 | 1 |
| Entered_Time | INTERVAL | 10 | 1 |
| Entered_By | CLOB | 51 | 1 |
| Release_Date | TIMESTAMP | 19 | 1 |
| Release_Time | INTERVAL | 10 | 1 |
| Release_DateTime_Stamp | INT32 | 11 | 1 |
| Release_Quantity | INT32 | 11 | 1 |
| Cost_Unit | CLOB | 20 | 1 |
| Item_Cost | REAL | 7 | 1 |
| StockProduct_Ticket_ID | CLOB | 10 | 1 |
| PackSlipItem_ID | CLOB | 10 | 1 |
| Kit_Product_ID | CLOB | 10 | 1 |
| Kit_Part_Number | CLOB | 40 | 1 |
| Notes | CLOB | 80 | 1 |
| Modified_Date | TIMESTAMP | 19 | 1 |
| Modified_Time | INTERVAL | 10 | 1 |
| Modified_By | CLOB | 51 | 1 |
| Modification_Count | INT32 | 11 | 1 |
| Is_User_Made | BOOLEAN | 5 | 1 |
| Location | CLOB | 40 | 1 |
| PK_UUID | UUID | 0 | 1 |
| Cost_Unit_Local | CLOB | 20 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |
| newTimeDateStamp | CLOB | 255 | 1 |

### SalesTax_Preferences

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| State_Province | CLOB | 25 | 1 |
| Country | CLOB | 25 | 1 |
| GL_Acct_Number | CLOB | 13 | 1 |
| GL_Acct_Name | CLOB | 40 | 1 |
| TaxFreight | BOOLEAN | 5 | 1 |
| TaxPlateChanges | BOOLEAN | 5 | 1 |
| TaxColorChanges | BOOLEAN | 5 | 1 |
| Employee_Number | CLOB | 10 | 1 |
| Employee_Name | CLOB | 60 | 1 |
| RemindEvery_X_Days | INT32 | 11 | 1 |
| NextReminder | TIMESTAMP | 19 | 1 |
| LastReminder | TIMESTAMP | 19 | 1 |
| ListCertsExpireIn_X_Days | INT32 | 11 | 1 |
| BadRegionsMessage | BLOB | 0 | 1 |
| TaxOnPurchases_Show | BOOLEAN | 5 | 1 |
| TaxName | CLOB | 80 | 1 |
| ShowVATCodesOnTaxTypes | BOOLEAN | 5 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### SalesTax_RegionTypes

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| Region_ID | INT32 | 11 | 1 |
| TaxType_ID | INT32 | 11 | 1 |
| TaxType_Rate | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### SalesTax_Regions

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| RegionName | CLOB | 80 | 1 |
| Address_Default | BOOLEAN | 5 | 1 |
| RegionState | CLOB | 25 | 1 |
| RegionCountry | CLOB | 25 | 1 |
| RegionRate | REAL | 7 | 1 |
| NumberOfTaxTypes | INT32 | 11 | 1 |
| PrintEachTypeOnInvoice | BOOLEAN | 5 | 1 |
| Inactive | BOOLEAN | 5 | 1 |
| EnteredBy | CLOB | 50 | 1 |
| EnteredDate | TIMESTAMP | 19 | 1 |
| ModifyBy | CLOB | 50 | 1 |
| ModifyDate | TIMESTAMP | 19 | 1 |
| EnteredTime | INTERVAL | 10 | 1 |
| ModifyTime | INTERVAL | 10 | 1 |
| TaxOnPurchSupplierDefault | BOOLEAN | 5 | 1 |
| PrintTypeWhenZero | BOOLEAN | 5 | 1 |
| x11 | CLOB | 0 | 1 |
| x12 | CLOB | 0 | 1 |
| x13 | CLOB | 0 | 1 |
| x14 | CLOB | 0 | 1 |
| x15 | CLOB | 0 | 1 |
| x16 | CLOB | 0 | 1 |
| x17 | CLOB | 0 | 1 |
| x18 | CLOB | 0 | 1 |
| x19 | CLOB | 0 | 1 |
| x20 | CLOB | 0 | 1 |
| x21 | CLOB | 0 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### SalesTax_TaxTypes

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| TaxTypeName | CLOB | 80 | 1 |
| TaxTypeState | CLOB | 25 | 1 |
| TaxTypeCountry | CLOB | 25 | 1 |
| TaxTypeRate | REAL | 7 | 1 |
| InvoiceDescription | CLOB | 50 | 1 |
| FreightSubjectToTax | BOOLEAN | 5 | 1 |
| PlateChangesSubjectToTax | BOOLEAN | 5 | 1 |
| ColorChangesSubjectToTax | BOOLEAN | 5 | 1 |
| Inactive | BOOLEAN | 5 | 1 |
| GL_Acct_Name | CLOB | 40 | 1 |
| GL_Acct_Number | CLOB | 13 | 1 |
| EnteredBy | CLOB | 50 | 1 |
| EnteredDate | TIMESTAMP | 19 | 1 |
| ModifyBy | CLOB | 50 | 1 |
| ModifyDate | TIMESTAMP | 19 | 1 |
| EnteredTime | INTERVAL | 10 | 1 |
| ModifyTime | INTERVAL | 10 | 1 |
| GL_Acct_Name_Purchases | CLOB | 40 | 1 |
| GL_Acct_Num_Purchases | CLOB | 13 | 1 |
| VAT_Code_ID | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |
| Reverse_charge | BOOLEAN | 5 | 1 |
| Notional_rate | REAL | 7 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### SalesTax_VAT_Codes

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| VAT_Code | CLOB | 10 | 1 |
| Description | CLOB | 80 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### ScheduleDay

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| Sched_Date | TIMESTAMP | 19 | 1 |
| U1 | CLOB | 0 | 1 |
| Department | CLOB | 20 | 1 |
| Equipment_ID | CLOB | 20 | 1 |
| HoursAvailable | REAL | 7 | 1 |
| HoursScheduled | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### ScheduleDetail

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| Sched_Date | TIMESTAMP | 19 | 1 |
| Department | CLOB | 20 | 1 |
| Equipment_ID | CLOB | 20 | 1 |
| Ticket_ID | CLOB | 12 | 1 |
| CustomerName | CLOB | 40 | 1 |
| HoursScheduled | REAL | 7 | 1 |
| TaskNumber | INT32 | 11 | 1 |
| ScheduleDay_ID | INT32 | 11 | 1 |
| Ticket_Descr | CLOB | 60 | 1 |
| Tag | CLOB | 0 | 1 |
| Notes | CLOB | 0 | 1 |
| Status | CLOB | 20 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### Schedule_EquipGroup

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| Department | CLOB | 20 | 1 |
| Equipment_Group | CLOB | 40 | 1 |
| Equipment_ID_1 | CLOB | 20 | 1 |
| Equipment_ID_2 | CLOB | 20 | 1 |
| Equipment_ID_3 | CLOB | 20 | 1 |
| Equipment_ID_4 | CLOB | 20 | 1 |
| Equipment_ID_5 | CLOB | 20 | 1 |
| Equipment_ID_6 | CLOB | 20 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 255 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### Settings

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| PK_UUID | UUID | 0 | 0 |
| Name | CLOB | 255 | 1 |
| settingsObject | None | 0 | 1 |

### Stock

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| StockNum | CLOB | 10 | 1 |
| Classification | CLOB | 30 | 1 |
| SupplierNum | CLOB | 10 | 1 |
| MFGSpecNum | CLOB | 30 | 1 |
| MasterWidth | REAL | 7 | 1 |
| CostMSI | REAL | 7 | 1 |
| FaceStock | CLOB | 80 | 1 |
| FaceColor | CLOB | 15 | 1 |
| FaceCaliper | CLOB | 15 | 1 |
| LinerCaliper | CLOB | 15 | 1 |
| Adhesive | CLOB | 20 | 1 |
| AdhClass | CLOB | 20 | 1 |
| TotalInvMSI | REAL | 7 | 1 |
| InventoryCost | REAL | 7 | 1 |
| ULRecognized | BOOLEAN | 5 | 1 |
| CSACertified | BOOLEAN | 5 | 1 |
| TopCoat | CLOB | 30 | 1 |
| FreightMSI | REAL | 7 | 1 |
| Notes | CLOB | 0 | 1 |
| Inactive | BOOLEAN | 5 | 1 |
| SupplierName | CLOB | 80 | 1 |
| Location | CLOB | 12 | 1 |
| Caliper | REAL | 7 | 1 |
| InternetQuery | BOOLEAN | 5 | 1 |
| EnteredBy | CLOB | 50 | 1 |
| ModifiedBy | CLOB | 50 | 1 |
| EnteredDate | TIMESTAMP | 19 | 1 |
| ModifiedDate | TIMESTAMP | 19 | 1 |
| EnteredTime | INTERVAL | 10 | 1 |
| ModifiedTime | INTERVAL | 10 | 1 |
| InvMSI_Minimum | REAL | 7 | 1 |
| InvMSI_Maximum | REAL | 7 | 1 |
| VPB_VolumeTo_1 | INT32 | 11 | 1 |
| VPB_VolumeTo_2 | INT32 | 11 | 1 |
| VPB_VolumeTo_3 | INT32 | 11 | 1 |
| VPB_VolumeTo_4 | INT32 | 11 | 1 |
| VPB_VolumeFrom_2 | INT32 | 11 | 1 |
| VPB_VolumeFrom_3 | INT32 | 11 | 1 |
| VPB_VolumeFrom_4 | INT32 | 11 | 1 |
| VPB_VolumeFrom_5 | INT32 | 11 | 1 |
| VPB_CostMSI_2 | REAL | 7 | 1 |
| VPB_CostMSI_3 | REAL | 7 | 1 |
| VPB_CostMSI_4 | REAL | 7 | 1 |
| VPB_CostMSI_5 | REAL | 7 | 1 |
| VPB_FreightMSI_2 | REAL | 7 | 1 |
| VPB_FreightMSI_3 | REAL | 7 | 1 |
| VPB_FreightMSI_4 | REAL | 7 | 1 |
| VPB_FreightMSI_5 | REAL | 7 | 1 |
| StockSubstitute_1 | CLOB | 10 | 1 |
| StockSubstitute_2 | CLOB | 10 | 1 |
| StockSubstitute_3 | CLOB | 10 | 1 |
| EstimatedDeliveryTime | CLOB | 80 | 1 |
| LinkToDataSheet | CLOB | 0 | 1 |
| Notes_Other | CLOB | 0 | 1 |
| StockSubstitute_Notes | CLOB | 0 | 1 |
| PriceSpecifiedForEstimate | BOOLEAN | 5 | 1 |
| PriceChangeBy | CLOB | 50 | 1 |
| PriceChangeDate | TIMESTAMP | 19 | 1 |
| PriceChangeTime | INTERVAL | 10 | 1 |
| AreaToWeightFactor | REAL | 7 | 1 |
| VPB_VolumeTo_5 | INT32 | 11 | 1 |
| VPB_VolumeFrom_6 | INT32 | 11 | 1 |
| VPB_CostMSI_6 | REAL | 7 | 1 |
| VPB_FreightMSI_6 | REAL | 7 | 1 |
| VolumePriceForEstimates | INT32 | 11 | 1 |
| Is_Used_by_eStore | BOOLEAN | 5 | 1 |
| eTraxx_Description | CLOB | 80 | 1 |
| Is_OverLaminate | BOOLEAN | 5 | 1 |
| Yield_Area_Weight | REAL | 7 | 1 |
| Price_Weight | REAL | 7 | 1 |
| IsCoated_DigitalPress | BOOLEAN | 5 | 1 |
| StockNum_Uncoated | CLOB | 10 | 1 |
| StockNum_Coated | CLOB | 10 | 1 |
| Indigo_Type | CLOB | 30 | 1 |
| PK_UUID | UUID | 0 | 1 |
| Default_CoreSize | REAL | 7 | 1 |
| Currency_ID | INT32 | 11 | 1 |
| FX_VPB_CostMSI_1 | REAL | 7 | 1 |
| FX_VPB_CostMSI_2 | REAL | 7 | 1 |
| FX_VPB_CostMSI_3 | REAL | 7 | 1 |
| FX_VPB_CostMSI_4 | REAL | 7 | 1 |
| FX_VPB_CostMSI_5 | REAL | 7 | 1 |
| FX_VPB_CostMSI_6 | REAL | 7 | 1 |
| FX_VPB_FreightMSI_1 | REAL | 7 | 1 |
| FX_VPB_FreightMSI_2 | REAL | 7 | 1 |
| FX_VPB_FreightMSI_3 | REAL | 7 | 1 |
| FX_VPB_FreightMSI_4 | REAL | 7 | 1 |
| FX_VPB_FreightMSI_5 | REAL | 7 | 1 |
| FX_VPB_FreightMSI_6 | REAL | 7 | 1 |
| Currency_ExchangeRate | REAL | 7 | 1 |
| Total_InventoryWeight | REAL | 7 | 1 |
| FC_Price_Weight | REAL | 7 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |
| unused_95 | BOOLEAN | 5 | 1 |

### StockInventory

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| StockNum | CLOB | 10 | 1 |
| Width | REAL | 7 | 1 |
| Physical | INT32 | 11 | 1 |
| Allocated | INT32 | 11 | 1 |
| Available | INT32 | 11 | 1 |
| AvailableMSI | REAL | 7 | 1 |
| YTDFootage | INT32 | 11 | 1 |
| OnOrder | INT32 | 11 | 1 |
| DateDue | TIMESTAMP | 19 | 1 |
| SlitFootage | INT32 | 11 | 1 |
| SlitSize1 | REAL | 7 | 1 |
| SlitSize2 | REAL | 7 | 1 |
| SlitSize3 | REAL | 7 | 1 |
| SlitSize4 | REAL | 7 | 1 |
| SlitSize5 | REAL | 7 | 1 |
| SlitDone | BOOLEAN | 5 | 1 |
| SlitJobNum | CLOB | 10 | 1 |
| NumCut1 | INT16 | 6 | 1 |
| NumCut2 | INT16 | 6 | 1 |
| NumCut3 | INT16 | 6 | 1 |
| NumCut4 | INT16 | 6 | 1 |
| NumCut5 | INT16 | 6 | 1 |
| Is_Preferred | BOOLEAN | 5 | 1 |
| Width_Tolerance | REAL | 7 | 1 |
| Notes | CLOB | 0 | 1 |
| RollNum | INT16 | 6 | 1 |
| SlitFlag | BOOLEAN | 5 | 1 |
| MinimumWidth | REAL | 7 | 1 |
| MaximumWidth | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |
| AvailableWeight | REAL | 7 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |
| Tag | CLOB | 3 | 1 |

### StockProduct

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| ProductNo | CLOB | 30 | 1 |
| ProdClass | CLOB | 20 | 1 |
| ProdSubClass | CLOB | 35 | 1 |
| SupplierName | CLOB | 45 | 1 |
| SupplierNo | CLOB | 10 | 1 |
| Desc1 | CLOB | 80 | 1 |
| Desc2 | CLOB | 80 | 1 |
| Notes | CLOB | 0 | 1 |
| Available | INT32 | 11 | 1 |
| TotalCost | REAL | 7 | 1 |
| MinProduce | INT32 | 11 | 1 |
| MaxProduce | INT32 | 11 | 1 |
| PhysicalInv | INT32 | 11 | 1 |
| OnOrder | INT32 | 11 | 1 |
| PackageQty | INT32 | 11 | 1 |
| Location | CLOB | 40 | 1 |
| PriceMode | CLOB | 20 | 1 |
| SupplierPartNo | CLOB | 30 | 1 |
| SupplierNotes | CLOB | 0 | 1 |
| Cost | REAL | 7 | 1 |
| CaseQty | CLOB | 20 | 1 |
| BackOrdered | INT32 | 11 | 1 |
| Color | CLOB | 80 | 1 |
| Material | CLOB | 80 | 1 |
| Adhesive | CLOB | 80 | 1 |
| Alternate | CLOB | 80 | 1 |
| Customer_Num | CLOB | 10 | 1 |
| CustomerName | CLOB | 40 | 1 |
| Updated | TIMESTAMP | 19 | 1 |
| Part_Type | CLOB | 20 | 1 |
| Inactive | BOOLEAN | 5 | 1 |
| UPC | CLOB | 30 | 1 |
| Product_UniqueProdID | CLOB | 10 | 1 |
| Production_Waste | REAL | 7 | 1 |
| EnteredBy | CLOB | 50 | 1 |
| ModifiedBy | CLOB | 50 | 1 |
| EnteredDate | TIMESTAMP | 19 | 1 |
| ModifiedDate | TIMESTAMP | 19 | 1 |
| EnteredTime | INTERVAL | 10 | 1 |
| ModifiedTime | INTERVAL | 10 | 1 |
| Link_Factor | REAL | 7 | 1 |
| Inventory_Expires | INT32 | 11 | 1 |
| Weight | REAL | 7 | 1 |
| Box_Size | CLOB | 40 | 1 |
| InternetQuery | BOOLEAN | 5 | 1 |
| eTraxx_Forecast_Range | CLOB | 80 | 1 |
| eTraxx_Forecast_Quantity | INT32 | 11 | 1 |
| Releases_Allowed_Default | INT32 | 11 | 1 |
| Commission | REAL | 7 | 1 |
| Is_Location_UsedBy_Consignment | BOOLEAN | 5 | 1 |
| Is_LinkedCustomPricesUsed | BOOLEAN | 5 | 1 |
| Product_Image | BLOB | 0 | 1 |
| Product_Image_Size | REAL | 7 | 1 |
| PriceMode_Local | CLOB | 20 | 1 |
| PK_UUID | UUID | 0 | 1 |
| PictDisplayFormat | CLOB | 30 | 1 |
| File_Name | CLOB | 0 | 1 |
| Currency_ID | INT32 | 11 | 1 |
| Currency_ExchangeRate | REAL | 7 | 1 |
| FC_Cost | REAL | 7 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |
| Tag | CLOB | 3 | 1 |
| invStatus | CLOB | 0 | 1 |
| invStatus_Org | CLOB | 255 | 1 |
| LinkedCustomPriceNum | CLOB | 10 | 1 |

### StockProduct_XML_Order

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| StockProductTicket_ID | CLOB | 10 | 1 |
| Receipt_ID | CLOB | 80 | 1 |
| Document_Name | CLOB | 80 | 1 |
| Document_Source | BLOB | 0 | 1 |
| Created_Date | TIMESTAMP | 19 | 1 |
| Created_Time | INTERVAL | 10 | 1 |
| Is_Document_Processed | BOOLEAN | 5 | 1 |
| Is_XML_DTD_Valid | BOOLEAN | 5 | 1 |
| Are_RequiredValues_Given | BOOLEAN | 5 | 1 |
| Error_Message | CLOB | 0 | 1 |
| PickingSlip_Printed | BOOLEAN | 5 | 1 |
| PK_UUID | UUID | 0 | 1 |

### Supplier

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| Number | CLOB | 10 | 1 |
| Company | CLOB | 80 | 1 |
| Addr1 | CLOB | 255 | 1 |
| Addr2 | CLOB | 255 | 1 |
| City | CLOB | 40 | 1 |
| State_Province | CLOB | 25 | 1 |
| Zip | CLOB | 15 | 1 |
| Phone | CLOB | 20 | 1 |
| FAX | CLOB | 20 | 1 |
| Sales | CLOB | 80 | 1 |
| KeyWords | CLOB | 80 | 1 |
| Notes | CLOB | 0 | 1 |
| Key_Words_subtable | INT32 | 11 | 1 |
| CustServ | CLOB | 80 | 1 |
| SupType | CLOB | 20 | 1 |
| AcctNum | CLOB | 25 | 1 |
| Country | CLOB | 25 | 1 |
| EntryDate | TIMESTAMP | 19 | 1 |
| EntryBy | CLOB | 50 | 1 |
| ModifyDate | TIMESTAMP | 19 | 1 |
| ModifyBy | CLOB | 50 | 1 |
| A4LinkDate | TIMESTAMP | 19 | 1 |
| SendToA4 | CLOB | 20 | 1 |
| A4LinkBatchID | INT32 | 11 | 1 |
| A4VendorID | INT32 | 11 | 1 |
| NetDayDue | INT32 | 11 | 1 |
| DiscountPercent | REAL | 7 | 1 |
| DueWithin | INT32 | 11 | 1 |
| DueBy | INT32 | 11 | 1 |
| InternalDept | BOOLEAN | 5 | 1 |
| Terms | CLOB | 45 | 1 |
| RemitTo_Addr1 | CLOB | 255 | 1 |
| RemitTo_Addr2 | CLOB | 255 | 1 |
| RemitTo_City | CLOB | 40 | 1 |
| RemitTo_State | CLOB | 25 | 1 |
| RemitTo_Zip | CLOB | 15 | 1 |
| RemitTo_Country | CLOB | 25 | 1 |
| Tax_ID | CLOB | 20 | 1 |
| Send_1099 | BOOLEAN | 5 | 1 |
| PaymentsOldSystem | REAL | 7 | 1 |
| eCommerceSupplier_Fasson | BOOLEAN | 5 | 1 |
| FassonConnectCurrency | CLOB | 30 | 1 |
| FassonConnectFTPServerName | CLOB | 80 | 1 |
| FassonConnectUserName | CLOB | 40 | 1 |
| FassonConnectPassword | CLOB | 40 | 1 |
| FassonConnectFTPDirectory | CLOB | 80 | 1 |
| FSS_IP_1 | CLOB | 3 | 1 |
| FSS_IP_2 | CLOB | 3 | 1 |
| FSS_IP_3 | CLOB | 3 | 1 |
| FSS_IP_4 | CLOB | 3 | 1 |
| FSS_IP_Port | CLOB | 6 | 1 |
| RollExchangeDirectory | CLOB | 80 | 1 |
| FSS_UseFassonRoll_IDs | BOOLEAN | 5 | 1 |
| Rollxchange_CustomerID | CLOB | 20 | 1 |
| Inactive | BOOLEAN | 5 | 1 |
| eCommerceSupplier | CLOB | 60 | 1 |
| eCommerceSupplier_Raflatac | BOOLEAN | 5 | 1 |
| eCommerce_RaflatacAddressID | CLOB | 40 | 1 |
| SOAP_Server_UserName | CLOB | 0 | 1 |
| SOAP_Server_Password | CLOB | 0 | 1 |
| SupplierNum_b4_LT | CLOB | 80 | 1 |
| TypeOf1099 | CLOB | 20 | 1 |
| eCommerceSupplier_GreenBay | BOOLEAN | 5 | 1 |
| SOAP_Server_URL | CLOB | 0 | 1 |
| EntryTime | INTERVAL | 10 | 1 |
| ModifyTime | INTERVAL | 10 | 1 |
| eCommerceSupplier_MACtac | BOOLEAN | 5 | 1 |
| eCommerceSupplier_Spinnaker | BOOLEAN | 5 | 1 |
| eCommerceSupplier_Technicote | BOOLEAN | 5 | 1 |
| QT_Supplier_Default_Art_PO | BOOLEAN | 5 | 1 |
| QT_Supplier_Default_Plate_PO | BOOLEAN | 5 | 1 |
| eCommerceSupplier_RaflatacEuro | BOOLEAN | 5 | 1 |
| SOAP_Server_NameSpace | CLOB | 0 | 1 |
| eCommerceSupplier_Acucote | BOOLEAN | 5 | 1 |
| TaxRegionID | INT32 | 11 | 1 |
| eCommerceSupplier_FLEXcon | BOOLEAN | 5 | 1 |
| eCommerce_PO_email | CLOB | 0 | 1 |
| eCommerceSupplier_FassonEuro | BOOLEAN | 5 | 1 |
| Currency_ID | INT32 | 11 | 1 |
| EP_RoutingNumber | CLOB | 0 | 1 |
| EP_AccountNumber | CLOB | 0 | 1 |
| EP_OtherNumber | CLOB | 0 | 1 |
| EP_Email | CLOB | 80 | 1 |
| RemitTo_Phone | CLOB | 20 | 1 |
| Main_Email | CLOB | 0 | 1 |
| Rating | CLOB | 20 | 1 |
| PreferredShipper | CLOB | 40 | 1 |
| DiscountRates | CLOB | 20 | 1 |
| RestrictedAccessSupplier | BOOLEAN | 5 | 1 |
| eCommerceSupplier_Master | BOOLEAN | 5 | 1 |
| Website | CLOB | 0 | 1 |
| eCommerceSupplier_Wausau | BOOLEAN | 5 | 1 |
| eCommerceSupplier_STA | BOOLEAN | 5 | 1 |
| eCommerceSupplier_Roto | BOOLEAN | 5 | 1 |
| Bank_ID | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |
| eCommerceSupplier_Herma | BOOLEAN | 5 | 1 |
| eCommerceSupplier_IPaddress | CLOB | 255 | 1 |
| eCommerceSupplier_Username | CLOB | 255 | 1 |
| eCommerceSupplier_Password | CLOB | 255 | 1 |
| paymentType | CLOB | 45 | 1 |
| eCommerceSupplier_HermaUK | BOOLEAN | 5 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |
| unused_105 | BOOLEAN | 5 | 1 |

### Supplier_Activity

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| SupplierNum | CLOB | 10 | 1 |
| Employee_ID | CLOB | 10 | 1 |
| Employee_Name | CLOB | 60 | 1 |
| Creation_Date | TIMESTAMP | 19 | 1 |
| Creation_Time | INTERVAL | 10 | 1 |
| Contact_ID | CLOB | 10 | 1 |
| Contact_Name | CLOB | 50 | 1 |
| Contact_Extension | CLOB | 10 | 1 |
| Call_Back | TIMESTAMP | 19 | 1 |
| Activity | CLOB | 40 | 1 |
| Notes | CLOB | 0 | 1 |
| Email_To_Address | CLOB | 0 | 1 |
| Email_Subject | CLOB | 0 | 1 |
| Email_Message | CLOB | 0 | 1 |
| Email_Sent | BOOLEAN | 5 | 1 |
| Contact_Phone | CLOB | 20 | 1 |
| PK_UUID | UUID | 0 | 1 |

### Supplier_Contact

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| SupplierNum | CLOB | 10 | 1 |
| Honorific_Prefix | CLOB | 10 | 1 |
| FirstName | CLOB | 20 | 1 |
| LastName | CLOB | 20 | 1 |
| Title | CLOB | 20 | 1 |
| Phone | CLOB | 20 | 1 |
| Department | CLOB | 20 | 1 |
| Extension | CLOB | 10 | 1 |
| Fax | CLOB | 20 | 1 |
| Email | CLOB | 60 | 1 |
| Pager | CLOB | 20 | 1 |
| Cell | CLOB | 20 | 1 |
| EnteredBy | CLOB | 50 | 1 |
| EnteredDate | TIMESTAMP | 19 | 1 |
| EnteredTime | INTERVAL | 10 | 1 |
| ModifyBy | CLOB | 50 | 1 |
| ModifyDate | TIMESTAMP | 19 | 1 |
| ModifyTime | INTERVAL | 10 | 1 |
| Notes | CLOB | 0 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### Supplier_GL_Defaults

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| Supplier_ID | CLOB | 10 | 1 |
| AccountNumber | CLOB | 13 | 1 |
| AccountName | CLOB | 40 | 1 |
| Percent_Applied | REAL | 7 | 1 |
| U1 | CLOB | 0 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### Supplier_eCommerce

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 0 |
| SupplierNumber | CLOB | 10 | 1 |
| AccountNumber | CLOB | 25 | 1 |
| ShipToID | CLOB | 25 | 1 |
| Tag | CLOB | 3 | 1 |
| eCommerceSupplierName | CLOB | 80 | 1 |
| Send_URL | CLOB | 255 | 1 |
| Send_Username | CLOB | 40 | 1 |
| Send_Password | CLOB | 40 | 1 |
| Send_Other | CLOB | 255 | 1 |
| Receive_URL | CLOB | 255 | 1 |
| Receive_Username | CLOB | 80 | 1 |
| Receive_Password | CLOB | 80 | 1 |
| Receive_Other | CLOB | 80 | 1 |
| UseSupplierRoll_IDs | BOOLEAN | 5 | 1 |
| Currency | CLOB | 40 | 1 |
| RollExchangeDirectory | CLOB | 80 | 1 |
| RollExchange_CustomerID | CLOB | 20 | 1 |
| PK_UUID | UUID | 0 | 1 |

### TLI_Status

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| TicketItem_ID | CLOB | 10 | 1 |
| Shipping_Status | CLOB | 20 | 1 |
| PK_UUID | UUID | 0 | 1 |

### Table_oc

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| Yo_Ho_Ho | BOOLEAN | 5 | 1 |
| Blank | BOOLEAN | 5 | 1 |
| Alpha20_1 | CLOB | 20 | 1 |
| Real_1 | REAL | 7 | 1 |
| Alpha10_2 | CLOB | 20 | 1 |
| Alpha40_3 | CLOB | 20 | 1 |
| Alpha20_4 | CLOB | 20 | 1 |
| Text_5a | CLOB | 0 | 1 |
| Text_2 | CLOB | 0 | 1 |
| Text_3 | CLOB | 0 | 1 |
| Text_4 | CLOB | 0 | 1 |
| Text_5 | CLOB | 0 | 1 |
| Text_6 | CLOB | 0 | 1 |
| Text_7 | CLOB | 0 | 1 |
| PK_UUID | UUID | 0 | 1 |

### Tax_Adjustments

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| InvoiceNum | CLOB | 10 | 1 |
| AdjustDate | TIMESTAMP | 19 | 1 |
| AdjustSourceDoc | CLOB | 50 | 1 |
| AdjustType | CLOB | 50 | 1 |
| SalesTaxRegionID | INT32 | 11 | 1 |
| SalesTaxRegionName | CLOB | 80 | 1 |
| SalesTaxRegionRate | REAL | 7 | 1 |
| TaxTypeID | INT32 | 11 | 1 |
| TaxTypeName | CLOB | 80 | 1 |
| TaxTypeState | CLOB | 25 | 1 |
| TaxTypeCountry | CLOB | 25 | 1 |
| TaxTypeRate | REAL | 7 | 1 |
| TotalSaleAmount | REAL | 7 | 1 |
| Taxable | BOOLEAN | 5 | 1 |
| Resale | BOOLEAN | 5 | 1 |
| ExemptSaleAmount | REAL | 7 | 1 |
| NonTaxableSaleAmount | REAL | 7 | 1 |
| ResaleAmount | REAL | 7 | 1 |
| TotalAmountSubjectToTax | REAL | 7 | 1 |
| SalesTaxAmount | REAL | 7 | 1 |
| AP_Invoice_ID | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |
| glPrefix | CLOB | 3 | 1 |

### Tax_CashBasis_Payments

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| InvoiceNumber | CLOB | 20 | 1 |
| PaymentDate | TIMESTAMP | 19 | 1 |
| SourceDoc | CLOB | 50 | 1 |
| PaymentType | CLOB | 50 | 1 |
| SalesTaxRegionID | INT32 | 11 | 1 |
| SalesTaxRegionName | CLOB | 80 | 1 |
| SalesTaxRegionRate | REAL | 7 | 1 |
| TaxTypeID | INT32 | 11 | 1 |
| TaxTypeName | CLOB | 80 | 1 |
| TaxTypeState | CLOB | 25 | 1 |
| TaxTypeCountry | CLOB | 25 | 1 |
| TaxTypeRate | REAL | 7 | 1 |
| PaymentAmount | REAL | 7 | 1 |
| Taxable | BOOLEAN | 5 | 1 |
| ExemptAmount | REAL | 7 | 1 |
| NonTaxableAmount | REAL | 7 | 1 |
| TotalAmountSubjectToTax | REAL | 7 | 1 |
| TaxAmount | REAL | 7 | 1 |
| AP_Invoice_ID | INT32 | 11 | 1 |
| PaymentTo | CLOB | 50 | 1 |
| CheckNumber | CLOB | 80 | 1 |
| PK_UUID | UUID | 0 | 1 |

### Tax_CashBasis_Receipts

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| InvoiceNum | CLOB | 10 | 1 |
| ReceiptDate | TIMESTAMP | 19 | 1 |
| SourceDoc | CLOB | 50 | 1 |
| ReceiptType | CLOB | 50 | 1 |
| SalesTaxRegionID | INT32 | 11 | 1 |
| SalesTaxRegionName | CLOB | 80 | 1 |
| SalesTaxRegionRate | REAL | 7 | 1 |
| TaxTypeID | INT32 | 11 | 1 |
| TaxTypeName | CLOB | 80 | 1 |
| TaxTypeState | CLOB | 25 | 1 |
| TaxTypeCountry | CLOB | 25 | 1 |
| TaxTypeRate | REAL | 7 | 1 |
| ReceiptAmount | REAL | 7 | 1 |
| ReceiptFrom | CLOB | 50 | 1 |
| CheckNumber | CLOB | 30 | 1 |
| Taxable | BOOLEAN | 5 | 1 |
| Resale | BOOLEAN | 5 | 1 |
| ExemptAmount | REAL | 7 | 1 |
| NonTaxableAmount | REAL | 7 | 1 |
| ResaleAmount | REAL | 7 | 1 |
| TotalAmountSubjectToTax | REAL | 7 | 1 |
| TaxAmount | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |

### Template_4D_Write

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| Related_Table | INT32 | 11 | 1 |
| Related_ID | CLOB | 10 | 1 |
| Name | CLOB | 30 | 1 |
| Description | CLOB | 0 | 1 |
| Template_ | BLOB | 0 | 1 |
| PK_UUID | UUID | 0 | 1 |
| Pro_Template_ | None | 0 | 1 |

### TickItmStatus_to_AE_Event

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| TicketItem_WorkStatus | CLOB | 40 | 1 |
| BackStage_EventName | CLOB | 40 | 1 |
| BackStage_Ticket | CLOB | 40 | 1 |
| PK_UUID | UUID | 0 | 1 |

### Ticket

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| Number | CLOB | 12 | 1 |
| OrderDate | TIMESTAMP | 19 | 1 |
| Ship_by_Date | TIMESTAMP | 19 | 1 |
| ArtStat | CLOB | 20 | 1 |
| ProofStat | CLOB | 20 | 1 |
| PlateStat | CLOB | 20 | 1 |
| ToolStat | CLOB | 20 | 1 |
| HashIndex | CLOB | 20 | 1 |
| PressStat | CLOB | 20 | 1 |
| FinishStat | CLOB | 20 | 1 |
| ShipStat | CLOB | 8 | 1 |
| ArtDone | BOOLEAN | 5 | 1 |
| ProofDone | BOOLEAN | 5 | 1 |
| PlateDone | BOOLEAN | 5 | 1 |
| ToolsIn | BOOLEAN | 5 | 1 |
| StockIn | CLOB | 3 | 1 |
| PressDone | BOOLEAN | 5 | 1 |
| FinishDone | BOOLEAN | 5 | 1 |
| NoPlateChanges | INT32 | 11 | 1 |
| PrevJobNum | CLOB | 10 | 1 |
| GeneralDescr | CLOB | 50 | 1 |
| EstTime | REAL | 7 | 1 |
| CarrierWidth | REAL | 7 | 1 |
| OnTime | BOOLEAN | 5 | 1 |
| SizeAcross | REAL | 7 | 1 |
| SizeAround | REAL | 7 | 1 |
| ColSpace | REAL | 7 | 1 |
| RowSpace | REAL | 7 | 1 |
| LabelRepeat | REAL | 7 | 1 |
| NoAcross | INT16 | 6 | 1 |
| NoArounPlate | INT16 | 6 | 1 |
| NoColorChanges | INT32 | 11 | 1 |
| FinishType | CLOB | 15 | 1 |
| Pinfeed | BOOLEAN | 5 | 1 |
| LabelsPer_ | INT32 | 11 | 1 |
| NoLabAcrossFin | INT16 | 6 | 1 |
| CoreSize | REAL | 7 | 1 |
| FinalUnwind | CLOB | 15 | 1 |
| LabelsPerFold | INT16 | 6 | 1 |
| SheetPacktype | CLOB | 20 | 1 |
| Tab | REAL | 7 | 1 |
| Press | CLOB | 10 | 1 |
| MainTool | CLOB | 15 | 1 |
| CustPONum | CLOB | 25 | 1 |
| TurnBar | BOOLEAN | 5 | 1 |
| Image_Rotation | CLOB | 10 | 1 |
| ColumnPerf | REAL | 7 | 1 |
| RowPerf | REAL | 7 | 1 |
| OverRun | REAL | 7 | 1 |
| AutoAppl | BOOLEAN | 5 | 1 |
| CustomerNum | CLOB | 10 | 1 |
| EndUserNum | CLOB | 10 | 1 |
| StockNum1 | CLOB | 10 | 1 |
| StockWidth1 | REAL | 7 | 1 |
| EstFootage | INT32 | 11 | 1 |
| StockNum2 | CLOB | 10 | 1 |
| StockWidth2 | REAL | 7 | 1 |
| ToolNo2 | CLOB | 15 | 1 |
| StockNum3 | CLOB | 10 | 1 |
| StockWidth3 | REAL | 7 | 1 |
| Tool2Descr | CLOB | 15 | 1 |
| ITSAssocNum | CLOB | 10 | 1 |
| OTSAssocNum | CLOB | 10 | 1 |
| ShipVia | CLOB | 40 | 1 |
| ShippingInstruc | CLOB | 50 | 1 |
| ShipAttn | CLOB | 30 | 1 |
| MFGRepNum | CLOB | 10 | 1 |
| MFGRepComm | REAL | 7 | 1 |
| Notes | CLOB | 0 | 1 |
| DateDone | TIMESTAMP | 19 | 1 |
| ShipAttn_EmailAddress | CLOB | 60 | 1 |
| ShipLocation | CLOB | 80 | 1 |
| ShipAddr1 | CLOB | 255 | 1 |
| ShipAddr2 | CLOB | 255 | 1 |
| ShipCity | CLOB | 40 | 1 |
| ShipSt | CLOB | 25 | 1 |
| ShipZip | CLOB | 15 | 1 |
| BillLocation | CLOB | 80 | 1 |
| BillAddr1 | CLOB | 255 | 1 |
| BillAddr2 | CLOB | 255 | 1 |
| BillCity | CLOB | 40 | 1 |
| BillZip | CLOB | 15 | 1 |
| BillCountry | CLOB | 25 | 1 |
| ShippingStatus | CLOB | 16 | 1 |
| ShipCountry | CLOB | 25 | 1 |
| StockTicketType | INT16 | 6 | 1 |
| SalesCommission | REAL | 7 | 1 |
| Stock_Allocated | BOOLEAN | 5 | 1 |
| EndUserPO | CLOB | 30 | 1 |
| CustomerName | CLOB | 80 | 1 |
| ToolNo3 | CLOB | 15 | 1 |
| Tool3Descr | CLOB | 15 | 1 |
| ToolNo4 | CLOB | 15 | 1 |
| Tool4Descr | CLOB | 15 | 1 |
| ToolNo5 | CLOB | 15 | 1 |
| Tool5Descr | CLOB | 20 | 1 |
| CornerRadius | REAL | 7 | 1 |
| DateShipped | TIMESTAMP | 19 | 1 |
| OTSName | CLOB | 35 | 1 |
| TicketType | INT16 | 6 | 1 |
| TicQuantity | INT32 | 11 | 1 |
| ITSName | CLOB | 35 | 1 |
| ActFootage | INT32 | 11 | 1 |
| EstMRHrs | REAL | 7 | 1 |
| ActMRHrs | REAL | 7 | 1 |
| EstWuHrs | REAL | 7 | 1 |
| ActWuHrs | REAL | 7 | 1 |
| ShipAsOne | BOOLEAN | 5 | 1 |
| EarlyShipOK | BOOLEAN | 5 | 1 |
| EstRunHrs | REAL | 7 | 1 |
| ActRunHrs | REAL | 7 | 1 |
| EstFinHrs | REAL | 7 | 1 |
| ActualFanfoldHours | REAL | 7 | 1 |
| EstPackHrs | REAL | 7 | 1 |
| ActPackHrs | REAL | 7 | 1 |
| EstPressSpd | INT16 | 6 | 1 |
| ActPressSpd | INT16 | 6 | 1 |
| ActQuantity | INT32 | 11 | 1 |
| Act_MakeReady_Footage | INT32 | 11 | 1 |
| Is_Ink_In | BOOLEAN | 5 | 1 |
| Ink_Status | CLOB | 20 | 1 |
| EstTotal | REAL | 7 | 1 |
| ActTotalCost | REAL | 7 | 1 |
| EstStockCost | REAL | 7 | 1 |
| ActStockCost | REAL | 7 | 1 |
| EstFinMaterial | REAL | 7 | 1 |
| ActFinMaterial | REAL | 7 | 1 |
| BillCounty | CLOB | 20 | 1 |
| EstArtwork | REAL | 7 | 1 |
| ActArtwork | REAL | 7 | 1 |
| Shape | CLOB | 40 | 1 |
| TabPosition | BOOLEAN | 5 | 1 |
| LastModified | TIMESTAMP | 19 | 1 |
| StockDesc1 | CLOB | 80 | 1 |
| StockDesc2 | CLOB | 80 | 1 |
| StockDesc3 | CLOB | 80 | 1 |
| EndUserName | CLOB | 80 | 1 |
| MFGRepName | CLOB | 80 | 1 |
| BillState | CLOB | 25 | 1 |
| CustContact | CLOB | 60 | 1 |
| CSA | BOOLEAN | 5 | 1 |
| UL | BOOLEAN | 5 | 1 |
| ConsecNo | BOOLEAN | 5 | 1 |
| POTotal | REAL | 7 | 1 |
| TicketStatus | CLOB | 30 | 1 |
| PlateChangeCost | REAL | 7 | 1 |
| ColorChangeCost | REAL | 7 | 1 |
| MiscChargeDesc | CLOB | 30 | 1 |
| MiscCharge | REAL | 7 | 1 |
| CoreType | CLOB | 15 | 1 |
| RollLength | INT32 | 11 | 1 |
| RollUnit | CLOB | 7 | 1 |
| Tape | BOOLEAN | 5 | 1 |
| PriceMode | CLOB | 20 | 1 |
| StockProdDiscnt | REAL | 7 | 1 |
| Total_LineWeight | REAL | 7 | 1 |
| UserDef_MR_1 | BOOLEAN | 5 | 1 |
| UserDef_MR_2 | BOOLEAN | 5 | 1 |
| UserDef_MR_1_Lb | CLOB | 20 | 1 |
| UserDef_MR_2_Lb | CLOB | 20 | 1 |
| Priority | CLOB | 31 | 1 |
| OutsideDiameter | REAL | 7 | 1 |
| FinishNotes | CLOB | 80 | 1 |
| EstPressTime | REAL | 7 | 1 |
| RewindEquipNum | CLOB | 10 | 1 |
| RewindEquipNam | CLOB | 35 | 1 |
| SubTicket | BOOLEAN | 5 | 1 |
| AmortizePlateChanges | BOOLEAN | 5 | 1 |
| AmortizeColorChanges | BOOLEAN | 5 | 1 |
| EntryBy | CLOB | 50 | 1 |
| EntryDate | TIMESTAMP | 19 | 1 |
| Terms | CLOB | 45 | 1 |
| ActualPressHours | REAL | 7 | 1 |
| ActualTotalHours | REAL | 7 | 1 |
| ActualPressRate | REAL | 7 | 1 |
| ActualPressCost | REAL | 7 | 1 |
| ActualRewindingRate | REAL | 7 | 1 |
| ActualRewindingCost | REAL | 7 | 1 |
| ActualFanfoldRate | REAL | 7 | 1 |
| ActualFanFoldCost | REAL | 7 | 1 |
| ActualPackagingRate | REAL | 7 | 1 |
| ActualPackingLaborCost | REAL | 7 | 1 |
| ActualNumOfStockRolls | REAL | 7 | 1 |
| ActualFootage_StockRolls | REAL | 7 | 1 |
| ActualMSI_StockRolls | REAL | 7 | 1 |
| ActualBillings_NetOfSalesTax | REAL | 7 | 1 |
| ActualGrossMargin_Dollars | REAL | 7 | 1 |
| ActualGrossMargin_Percent | REAL | 7 | 1 |
| ActualRewindingHours | REAL | 7 | 1 |
| ActualTotalFinishing | REAL | 7 | 1 |
| ActualTotalLaborCosts | REAL | 7 | 1 |
| ActualTotalPOCosts | REAL | 7 | 1 |
| ActualTotalMatAndFreightCost | REAL | 7 | 1 |
| Est_SetupFootage | INT32 | 11 | 1 |
| Est_SpoilFootage | INT32 | 11 | 1 |
| ShipCounty | CLOB | 20 | 1 |
| Est_v_Act_Notes | CLOB | 0 | 1 |
| EstPostPressHours | REAL | 7 | 1 |
| ActPostPressHours | REAL | 7 | 1 |
| Act_OTHER_Hours | REAL | 7 | 1 |
| ActualPostPressLaborCost | REAL | 7 | 1 |
| CustContact_ID | CLOB | 10 | 1 |
| StockNotes | CLOB | 0 | 1 |
| SoldToEndUser | BOOLEAN | 5 | 1 |
| Sheet_Width | REAL | 7 | 1 |
| Sheet_Height | REAL | 7 | 1 |
| SlitOnRewind | BOOLEAN | 5 | 1 |
| ActualOtherLaborCost | REAL | 7 | 1 |
| ActualCommissionsCost | REAL | 7 | 1 |
| Is_AutoOrder | BOOLEAN | 5 | 1 |
| Ship_Address_ID | CLOB | 10 | 1 |
| Ship_TaxRegion_ID | INT32 | 11 | 1 |
| Bill_Address_ID | CLOB | 10 | 1 |
| Bill_TaxRegion_ID | INT32 | 11 | 1 |
| Internet_Submission | BOOLEAN | 5 | 1 |
| EntryTime | INTERVAL | 10 | 1 |
| ModifyTime | INTERVAL | 10 | 1 |
| ModifyBy | CLOB | 50 | 1 |
| ModifyDate | TIMESTAMP | 19 | 1 |
| Equip_ID | CLOB | 10 | 1 |
| Are_Tools_for_Equip | BOOLEAN | 5 | 1 |
| Equip_MakeReadyHours | REAL | 7 | 1 |
| Equip_WashUpHours | REAL | 7 | 1 |
| Equip_EstSpeed | INT32 | 11 | 1 |
| Equip_EstRunHrs | REAL | 7 | 1 |
| Equip_Actual_MR_Hours | REAL | 7 | 1 |
| Equip_Actual_MR_Length | INT32 | 11 | 1 |
| Equip_Actual_Length | INT32 | 11 | 1 |
| Equip_Actual_Run_Hours | REAL | 7 | 1 |
| Equip_Actual_WU_Hours | REAL | 7 | 1 |
| Equip_Actual_Speed | INT32 | 11 | 1 |
| Equip_EstTime | REAL | 7 | 1 |
| Equip_Actual_Hours | REAL | 7 | 1 |
| Equip_Actual_Rate | REAL | 7 | 1 |
| Equip_Actual_Cost | REAL | 7 | 1 |
| Equip_Status | CLOB | 20 | 1 |
| Equip_Done | BOOLEAN | 5 | 1 |
| Due_on_Site_Date | TIMESTAMP | 19 | 1 |
| CreditHoldOverride | BOOLEAN | 5 | 1 |
| Calculation_TimeStamp | INT32 | 11 | 1 |
| Use_TurretRewinder | BOOLEAN | 5 | 1 |
| Is_ActBillNetTax_UserModified | BOOLEAN | 5 | 1 |
| Currency_ID | INT32 | 11 | 1 |
| Currency_ExchangeRate | REAL | 7 | 1 |
| ESC_Art | BOOLEAN | 5 | 1 |
| ESC_Proof | BOOLEAN | 5 | 1 |
| ESC_Plate | BOOLEAN | 5 | 1 |
| ESC_Tool | BOOLEAN | 5 | 1 |
| ESC_Ink | BOOLEAN | 5 | 1 |
| ESC_Stock | BOOLEAN | 5 | 1 |
| ESC_Press | BOOLEAN | 5 | 1 |
| ESC_Equip | BOOLEAN | 5 | 1 |
| ESC_Finish | BOOLEAN | 5 | 1 |
| ESC_Ship | BOOLEAN | 5 | 1 |
| ESC_TickStat | BOOLEAN | 5 | 1 |
| ESS_Ship | BOOLEAN | 5 | 1 |
| ESS_TickStat | BOOLEAN | 5 | 1 |
| ES_CSR | BOOLEAN | 5 | 1 |
| ES_SalesRep | BOOLEAN | 5 | 1 |
| ShrinkSleeve_OverLap | REAL | 7 | 1 |
| ShrinkSleeve_LayFlat | REAL | 7 | 1 |
| ShrinkSleeve_CutHeight | REAL | 7 | 1 |
| Freight_AcctNo | CLOB | 20 | 1 |
| BackStage_ColorStrategy | CLOB | 40 | 1 |
| BackStage_SmartMarkSet | CLOB | 40 | 1 |
| Equip3_ID | CLOB | 10 | 1 |
| Equip3_MakeReadyHours | REAL | 7 | 1 |
| Equip3_WashUpHours | REAL | 7 | 1 |
| Equip3_EstSpeed | INT32 | 11 | 1 |
| Equip3_EstRunHrs | REAL | 7 | 1 |
| Equip3_EstTime | REAL | 7 | 1 |
| Equip3_Actual_Length | INT32 | 11 | 1 |
| Equip3_Actual_MR_Length | INT32 | 11 | 1 |
| Equip3_Actual_Speed | INT32 | 11 | 1 |
| Equip3_Actual_MR_Hours | REAL | 7 | 1 |
| Equip3_Actual_Run_Hours | REAL | 7 | 1 |
| Equip3_Actual_WU_Hours | REAL | 7 | 1 |
| Equip3_Actual_Hours | REAL | 7 | 1 |
| Equip3_Actual_Rate | REAL | 7 | 1 |
| Equip3_Actual_Cost | REAL | 7 | 1 |
| Equip3_Status | CLOB | 20 | 1 |
| Equip3_Done | BOOLEAN | 5 | 1 |
| Equip4_ID | CLOB | 10 | 1 |
| Equip4_MakeReadyHours | REAL | 7 | 1 |
| Equip4_WashUpHours | REAL | 7 | 1 |
| Equip4_EstSpeed | INT32 | 11 | 1 |
| Equip4_EstRunHrs | REAL | 7 | 1 |
| Equip4_EstTime | REAL | 7 | 1 |
| Equip4_Actual_Length | INT32 | 11 | 1 |
| Equip4_Actual_MR_Length | INT32 | 11 | 1 |
| Equip4_Actual_Speed | INT32 | 11 | 1 |
| Equip4_Actual_MR_Hours | REAL | 7 | 1 |
| Equip4_Actual_Run_Hours | REAL | 7 | 1 |
| Equip4_Actual_WU_Hours | REAL | 7 | 1 |
| Equip4_Actual_Hours | REAL | 7 | 1 |
| Equip4_Actual_Rate | REAL | 7 | 1 |
| Equip4_Actual_Cost | REAL | 7 | 1 |
| Equip4_Status | CLOB | 20 | 1 |
| Equip4_Done | BOOLEAN | 5 | 1 |
| BackStage_DefaultReportForm | CLOB | 40 | 1 |
| ESC_Equip3 | BOOLEAN | 5 | 1 |
| ESC_Equip4 | BOOLEAN | 5 | 1 |
| Equip_NoAcross | INT32 | 11 | 1 |
| Equip_NoAround | INT32 | 11 | 1 |
| Equip_NumUp_Multiplier | INT32 | 11 | 1 |
| Equip3_NoAcross | INT32 | 11 | 1 |
| Equip3_NoAround | INT32 | 11 | 1 |
| Equip3_NumUp_Multiplier | INT32 | 11 | 1 |
| Equip4_NoAcross | INT32 | 11 | 1 |
| Equip4_NoAround | INT32 | 11 | 1 |
| Equip4_NumUp_Multiplier | INT32 | 11 | 1 |
| JDF_Sent_On | CLOB | 40 | 1 |
| Tool_NumberAround | INT16 | 6 | 1 |
| Roto_Quote_Number | CLOB | 80 | 1 |
| Roto_Quote_Line_ID | CLOB | 80 | 1 |
| ID | INT32 | 11 | 1 |
| Screen_Ratio | CLOB | 20 | 1 |
| Schedule_Status | CLOB | 40 | 1 |
| Roto_CEL_Product_ID | CLOB | 20 | 1 |
| JDF_Note_to_DFE | CLOB | 255 | 1 |
| TicketStatus_Local | CLOB | 255 | 1 |
| TicketType_Local | CLOB | 0 | 1 |
| Currency_Rate_ID | INT32 | 11 | 1 |
| StockIn_Local | CLOB | 0 | 1 |
| FC_PlateChangeCost | REAL | 7 | 1 |
| FC_ColorChangeCost | REAL | 7 | 1 |
| FC_MiscCharge | REAL | 7 | 1 |
| FC_EstTotal | REAL | 7 | 1 |
| FC_POTotal | REAL | 7 | 1 |
| PlateChangeCost_Extended | REAL | 7 | 1 |
| FC_PlateChangeCost_Extended | REAL | 7 | 1 |
| ColorChangeCost_Extended | REAL | 7 | 1 |
| FC_ColorChangeCost_Extended | REAL | 7 | 1 |
| Customer_Total | REAL | 7 | 1 |
| FC_Customer_Total | REAL | 7 | 1 |
| JDF_Send_Msg | CLOB | 255 | 1 |
| ESC_Art_Sales | BOOLEAN | 5 | 1 |
| ESC_Equip_Sales | BOOLEAN | 5 | 1 |
| ESC_Equip3_Sales | BOOLEAN | 5 | 1 |
| ESC_Equip4_Sales | BOOLEAN | 5 | 1 |
| ESC_Finish_Sales | BOOLEAN | 5 | 1 |
| ESC_Ink_Sales | BOOLEAN | 5 | 1 |
| ESC_Plate_Sales | BOOLEAN | 5 | 1 |
| ESC_Press_Sales | BOOLEAN | 5 | 1 |
| ESC_Ship_Sales | BOOLEAN | 5 | 1 |
| ESC_Stock_Sales | BOOLEAN | 5 | 1 |
| ESC_TickStat_Sales | BOOLEAN | 5 | 1 |
| ESC_Tool_Sales | BOOLEAN | 5 | 1 |
| ESC_Proof_sales | BOOLEAN | 5 | 1 |
| ESS_Ship_Sales | BOOLEAN | 5 | 1 |
| ESS_TickStat_Sales | BOOLEAN | 5 | 1 |
| MiscChargeDesc1 | CLOB | 0 | 1 |
| MiscChargeDesc2 | CLOB | 0 | 1 |
| MiscChargeDesc3 | CLOB | 0 | 1 |
| MiscChargeDesc4 | CLOB | 0 | 1 |
| MiscCharge1 | REAL | 7 | 1 |
| MiscCharge2 | REAL | 7 | 1 |
| MiscCharge3 | REAL | 7 | 1 |
| MiscCharge4 | REAL | 7 | 1 |
| FC_MiscCharge1 | REAL | 7 | 1 |
| FC_MiscCharge2 | REAL | 7 | 1 |
| FC_MiscCharge3 | REAL | 7 | 1 |
| FC_MiscCharge4 | REAL | 7 | 1 |
| Frames_Lead_In | INT32 | 11 | 1 |
| Frames_Lead_Out | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |
| IsPrintReversed | BOOLEAN | 5 | 1 |
| FlexPack_Type | INT32 | 11 | 1 |
| TotalOrderWeight | REAL | 7 | 1 |
| TotalShipWeight | REAL | 7 | 1 |
| FlexPack_Height | REAL | 7 | 1 |
| FlexPack_Gusset | REAL | 7 | 1 |
| FlexPack_LeftTrim | REAL | 7 | 1 |
| FlexPack_RightTrim | REAL | 7 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |
| Tag | CLOB | 3 | 1 |
| IsStockDropShipped | BOOLEAN | 5 | 1 |
| Equip5_ID | CLOB | 10 | 1 |
| Equip5_MakeReadyHours | REAL | 7 | 1 |
| Equip5_WashUpHours | REAL | 7 | 1 |
| Equip5_EstSpeed | INT32 | 11 | 1 |
| Equip5_EstRunHrs | REAL | 7 | 1 |
| Equip5_EstTime | REAL | 7 | 1 |
| Equip5_Actual_Length | INT32 | 11 | 1 |
| Equip5_Actual_MR_Length | INT32 | 11 | 1 |
| Equip5_Actual_Speed | INT32 | 11 | 1 |
| Equip5_Actual_MR_Hours | REAL | 7 | 1 |
| Equip5_Actual_Run_Hours | REAL | 7 | 1 |
| Equip5_Actual_WU_Hours | REAL | 7 | 1 |
| Equip5_Actual_Hours | REAL | 7 | 1 |
| Equip5_Actual_Rate | REAL | 7 | 1 |
| Equip5_Actual_Cost | REAL | 7 | 1 |
| Equip5_Status | CLOB | 20 | 1 |
| Equip5_Done | BOOLEAN | 5 | 1 |
| ESC_Equip5 | BOOLEAN | 5 | 1 |
| Equip5_NoAcross | INT32 | 11 | 1 |
| Equip5_NoAround | INT32 | 11 | 1 |
| Equip5_NumUp_Multiplier | INT32 | 11 | 1 |
| ESC_Equip5_Sales | BOOLEAN | 5 | 1 |
| Equip6_ID | CLOB | 10 | 1 |
| Equip6_MakeReadyHours | REAL | 7 | 1 |
| Equip6_WashUpHours | REAL | 7 | 1 |
| Equip6_EstSpeed | INT32 | 11 | 1 |
| Equip6_EstRunHrs | REAL | 7 | 1 |
| Equip6_EstTime | REAL | 7 | 1 |
| Equip6_Actual_Length | INT32 | 11 | 1 |
| Equip6_Actual_MR_Length | INT32 | 11 | 1 |
| Equip6_Actual_Speed | INT32 | 11 | 1 |
| Equip6_Actual_MR_Hours | REAL | 7 | 1 |
| Equip6_Actual_Run_Hours | REAL | 7 | 1 |
| Equip6_Actual_WU_Hours | REAL | 7 | 1 |
| Equip6_Actual_Hours | REAL | 7 | 1 |
| Equip6_Actual_Rate | REAL | 7 | 1 |
| Equip6_Actual_Cost | REAL | 7 | 1 |
| Equip6_Status | CLOB | 20 | 1 |
| Equip6_Done | BOOLEAN | 5 | 1 |
| ESC_Equip6 | BOOLEAN | 5 | 1 |
| Equip6_NoAcross | INT32 | 11 | 1 |
| Equip6_NoAround | INT32 | 11 | 1 |
| Equip6_NumUp_Multiplier | INT32 | 11 | 1 |
| ESC_Equip6_Sales | BOOLEAN | 5 | 1 |
| Multi_No | CLOB | 10 | 1 |
| Multi_ShipTogether | BOOLEAN | 5 | 1 |
| Ship_EstMRHrs | REAL | 7 | 1 |
| Ship_EstRunHrs | REAL | 7 | 1 |
| Ship_EstWUHrs | REAL | 7 | 1 |
| Ship_EstPressTime | REAL | 7 | 1 |
| Ship_EstPressSpd | INT32 | 11 | 1 |
| Ship_Equip_MakeReadyHours | REAL | 7 | 1 |
| Ship_Equip_EstRunHrs | REAL | 7 | 1 |
| Ship_Equip_WashUpHours | REAL | 7 | 1 |
| Ship_Equip_EstTime | REAL | 7 | 1 |
| Ship_Equip_EstSpeed | INT32 | 11 | 1 |
| Ship_EstFinHrs | REAL | 7 | 1 |
| Ship_EstPackHrs | REAL | 7 | 1 |
| Ship_EstPostPressHours | REAL | 7 | 1 |
| Ship_EstEstTime | REAL | 7 | 1 |
| Ship_EstFootage | REAL | 7 | 1 |
| Ship_EstStockCost | REAL | 7 | 1 |
| Tool_NumberAround_Eq2 | INT16 | 6 | 1 |
| Tool_NumberAround_Eq3 | INT16 | 6 | 1 |
| Tool_NumberAround_Eq4 | INT16 | 6 | 1 |
| Tool_NumberAround_Eq5 | INT16 | 6 | 1 |
| Tool_NumberAround_Eq6 | INT16 | 6 | 1 |
| Ship_Est_SpoilFootage | INT32 | 11 | 1 |
| Ship_Equip3_EstTime | REAL | 7 | 1 |
| Ship_Equip3_EstSpeed | INT32 | 11 | 1 |
| Ship_Equip3_MakeReadyHours | REAL | 7 | 1 |
| Ship_Equip3_EstRunHrs | REAL | 7 | 1 |
| Ship_Equip3_WashUpHours | REAL | 7 | 1 |
| Ship_Equip4_EstTime | REAL | 7 | 1 |
| Ship_Equip4_EstSpeed | INT32 | 11 | 1 |
| Ship_Equip4_MakeReadyHours | REAL | 7 | 1 |
| Ship_Equip4_EstRunHrs | REAL | 7 | 1 |
| Ship_Equip4_WashUpHours | REAL | 7 | 1 |
| Ship_Equip5_EstTime | REAL | 7 | 1 |
| Ship_Equip5_EstSpeed | INT32 | 11 | 1 |
| Ship_Equip5_MakeReadyHours | REAL | 7 | 1 |
| Ship_Equip5_EstRunHrs | REAL | 7 | 1 |
| Ship_Equip5_WashUpHours | REAL | 7 | 1 |
| Ship_Equip6_EstTime | REAL | 7 | 1 |
| Ship_Equip6_EstSpeed | INT32 | 11 | 1 |
| Ship_Equip6_MakeReadyHours | REAL | 7 | 1 |
| Ship_Equip6_EstRunHrs | REAL | 7 | 1 |
| Ship_Equip6_WashUpHours | REAL | 7 | 1 |
| Origin_Tag | CLOB | 3 | 1 |
| Equip_EstFootage | INT32 | 11 | 1 |
| Equip3_EstFootage | INT32 | 11 | 1 |
| Equip4_EstFootage | INT32 | 11 | 1 |
| Equip5_EstFootage | INT32 | 11 | 1 |
| Equip6_EstFootage | INT32 | 11 | 1 |
| Press_EstFootage | INT32 | 11 | 1 |

### TicketItem

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| TicketNumber | CLOB | 12 | 1 |
| ProductNumber | CLOB | 30 | 1 |
| Description | CLOB | 80 | 1 |
| NoColors | INT16 | 6 | 1 |
| ColorDescr | CLOB | 80 | 1 |
| NoFloods | INT16 | 6 | 1 |
| Desc2 | CLOB | 80 | 1 |
| OrderQuantity | INT32 | 11 | 1 |
| MachineCount | INT32 | 11 | 1 |
| JobType | CLOB | 20 | 1 |
| Location | CLOB | 40 | 1 |
| CostM | REAL | 7 | 1 |
| ConsecNo | CLOB | 20 | 1 |
| PriceM | REAL | 7 | 1 |
| UniquePrice | BOOLEAN | 5 | 1 |
| PriceMode | CLOB | 20 | 1 |
| StockProductID | CLOB | 10 | 1 |
| LineTotal | REAL | 7 | 1 |
| StckPrdShipStat | CLOB | 20 | 1 |
| UniqueProdID | CLOB | 10 | 1 |
| Equip_NoColors | INT16 | 6 | 1 |
| Equip_NoFloods | INT16 | 6 | 1 |
| PO_Number | CLOB | 30 | 1 |
| Unit_Weight | REAL | 7 | 1 |
| Line_Weight | REAL | 7 | 1 |
| Work_Status | CLOB | 40 | 1 |
| Assigned | CLOB | 40 | 1 |
| Art | BOOLEAN | 5 | 1 |
| Proof | BOOLEAN | 5 | 1 |
| Plate | BOOLEAN | 5 | 1 |
| Art_Ticket | BOOLEAN | 5 | 1 |
| Proof_Ticket | BOOLEAN | 5 | 1 |
| Plate_Ticket | BOOLEAN | 5 | 1 |
| Art_Item | BOOLEAN | 5 | 1 |
| Proof_Item | BOOLEAN | 5 | 1 |
| Plate_Item | BOOLEAN | 5 | 1 |
| Proof_Out | TIMESTAMP | 19 | 1 |
| Press_Null_Cycles | INT32 | 11 | 1 |
| Equip_Null_Cycles | INT32 | 11 | 1 |
| eTraxx_Customer_Notes | CLOB | 80 | 1 |
| Equip3_NoColors | INT16 | 6 | 1 |
| Equip3_NoFloods | INT16 | 6 | 1 |
| Equip3_Null_Cycles | INT16 | 6 | 1 |
| Equip4_NoColors | INT16 | 6 | 1 |
| Equip4_NoFloods | INT16 | 6 | 1 |
| Equip4_Null_Cycles | INT16 | 6 | 1 |
| FC_PriceM | REAL | 7 | 1 |
| FC_LineTotal | REAL | 7 | 1 |
| JobType_Local | CLOB | 255 | 1 |
| PK_UUID | UUID | 0 | 1 |
| PriceMode_Local | CLOB | 20 | 1 |
| ediLineNumber | CLOB | 20 | 1 |
| AVL_01 | BOOLEAN | 5 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |
| ProdRevisionNo | CLOB | 20 | 1 |
| Equip5_NoColors | INT16 | 6 | 1 |
| Equip5_NoFloods | INT16 | 6 | 1 |
| Equip5_Null_Cycles | INT16 | 6 | 1 |
| Equip6_NoColors | INT16 | 6 | 1 |
| Equip6_NoFloods | INT16 | 6 | 1 |
| Equip6_Null_Cycles | INT16 | 6 | 1 |
| Equip_ColorDescr | CLOB | 80 | 1 |
| Equip3_ColorDescr | CLOB | 80 | 1 |
| Equip4_ColorDescr | CLOB | 80 | 1 |
| Equip5_ColorDescr | CLOB | 80 | 1 |
| Equip6_ColorDescr | CLOB | 80 | 1 |

### Ticket_Activity

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| Ticket_ID | CLOB | 12 | 1 |
| Employee_ID | CLOB | 10 | 1 |
| Employee_Name | CLOB | 60 | 1 |
| Creation_Date | TIMESTAMP | 19 | 1 |
| Creation_Time | INTERVAL | 10 | 1 |
| Contact_ID | CLOB | 10 | 1 |
| Contact_Name | CLOB | 50 | 1 |
| Contact_Phone | CLOB | 20 | 1 |
| Contact_Extension | CLOB | 10 | 1 |
| Call_Back | TIMESTAMP | 19 | 1 |
| Activity | CLOB | 40 | 1 |
| Notes | CLOB | 0 | 1 |
| Email_To_Address | CLOB | 0 | 1 |
| Email_Subject | CLOB | 0 | 1 |
| Email_Message | CLOB | 0 | 1 |
| Email_Sent | BOOLEAN | 5 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### Ticket_BillOfMaterials

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| Ticket_Number | CLOB | 12 | 1 |
| TicketItem_ID | CLOB | 10 | 1 |
| UniqueProdID | CLOB | 10 | 1 |
| TicketItem_Quantity | INT32 | 11 | 1 |
| Inventory_ID | CLOB | 10 | 1 |
| Quantity_Part | REAL | 7 | 1 |
| Quantity_Label | INT32 | 11 | 1 |
| Quantity_TotalNeeded | REAL | 7 | 1 |
| Quantity_TotalUsed | REAL | 7 | 1 |
| TicketItem_ID_i | INT32 | 11 | 1 |
| Product_BOM_ID | INT32 | 11 | 1 |
| Product_Number | CLOB | 20 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### Ticket_CommonStock

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| TicketNumber | CLOB | 12 | 1 |
| StockNum | CLOB | 10 | 1 |
| Width | REAL | 7 | 1 |
| Description | CLOB | 80 | 1 |
| Caliper | REAL | 7 | 1 |
| StockType | CLOB | 20 | 1 |
| Classification | CLOB | 30 | 1 |
| SupplierNumber | CLOB | 10 | 1 |
| SupplierName | CLOB | 80 | 1 |
| PK_UUID | UUID | 0 | 1 |
| StockIn | CLOB | 3 | 1 |
| IsOverride | INT16 | 6 | 1 |
| RoutingNo | INT16 | 6 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### Ticket_FilePlan

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| TIcket_ID | CLOB | 10 | 1 |
| TicketItem_ID | CLOB | 20 | 1 |
| Product_UniqueID | CLOB | 10 | 1 |
| Order_Quantity | INT32 | 11 | 1 |
| Product_Number | CLOB | 40 | 1 |
| Product_Description | CLOB | 80 | 1 |
| FilePlate_Name | CLOB | 40 | 1 |
| FilePlate_Number | INT32 | 11 | 1 |
| FilePlate_TotalNumber | INT32 | 11 | 1 |
| Item_Order_Number | INT32 | 11 | 1 |
| Number_Of_Items_On_Plate | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### Ticket_JDF_Out

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| TicketNumber | CLOB | 12 | 1 |
| TicketItemNumber | CLOB | 10 | 1 |
| UniqueProdID | CLOB | 10 | 1 |
| ProductNumber | CLOB | 20 | 1 |
| JDF_Document | BLOB | 0 | 1 |
| Created_Date | TIMESTAMP | 19 | 1 |
| Created_Time | INTERVAL | 10 | 1 |
| Created_By | CLOB | 50 | 1 |
| Write_Status | CLOB | 20 | 1 |
| Write_Date | TIMESTAMP | 19 | 1 |
| Write_Time | INTERVAL | 10 | 1 |
| ScanLog_ID | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |

### Ticket_Tools

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| TicketNumber | CLOB | 12 | 1 |
| RoutingNo | INT16 | 6 | 1 |
| ToolNo | CLOB | 15 | 1 |
| ToolDescr | CLOB | 20 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### Ticket_UserDefined

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| EquipUserDefined_ID | INT32 | 11 | 1 |
| TicketNumber | CLOB | 12 | 1 |
| Description | CLOB | 20 | 1 |
| UseThisOption | BOOLEAN | 5 | 1 |
| Notes | CLOB | 60 | 1 |
| Print_On_Reports | BOOLEAN | 5 | 1 |
| Order_in_List | INT32 | 11 | 1 |
| Press_Number | CLOB | 10 | 1 |
| Option_Multiplier | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### TimeCard

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| AssocNo | CLOB | 10 | 1 |
| Ticket_No | CLOB | 12 | 1 |
| WorkOperation | CLOB | 20 | 1 |
| SDate | TIMESTAMP | 19 | 1 |
| EDate | TIMESTAMP | 19 | 1 |
| STime | INTERVAL | 10 | 1 |
| ETime | INTERVAL | 10 | 1 |
| Elapsed | INTERVAL | 10 | 1 |
| Closed | BOOLEAN | 5 | 1 |
| FinishedPieces | INT32 | 11 | 1 |
| PressNo | CLOB | 10 | 1 |
| FootUsed | INT32 | 11 | 1 |
| Totalizer | CLOB | 20 | 1 |
| Notes | CLOB | 0 | 1 |
| OffPress | BOOLEAN | 5 | 1 |
| Packaged | BOOLEAN | 5 | 1 |
| Labels_Est_to_Produce | REAL | 7 | 1 |
| Labels_Act_Net | REAL | 7 | 1 |
| Labels_Act_Waste | REAL | 7 | 1 |
| Labels_Act_Gross | REAL | 7 | 1 |
| Length_Est_Required | REAL | 7 | 1 |
| Length_Act_Net | REAL | 7 | 1 |
| Length_Act_Waste | REAL | 7 | 1 |
| Length_Act_Gross | REAL | 7 | 1 |
| Speed_Est_Length_Min | REAL | 7 | 1 |
| Speed_Act_Length_Min | REAL | 7 | 1 |
| Speed_Act_Labels_Min | REAL | 7 | 1 |
| Time_Est_Total | REAL | 7 | 1 |
| SC_MasterEvent_Code | CLOB | 255 | 1 |
| SC_Event_ID | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |
| Ticket_PressEquip | CLOB | 255 | 1 |
| Ticket_PressEquip_Local | CLOB | 255 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |
| Tag | CLOB | 3 | 1 |
| workShift | CLOB | 20 | 1 |

### TimeCard_Operation

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| WorkOperation | CLOB | 20 | 1 |
| Operation_Old | CLOB | 20 | 1 |
| Chargable | BOOLEAN | 5 | 1 |
| Sort_Order | REAL | 7 | 1 |
| Rate | REAL | 7 | 1 |
| Color | INT32 | 11 | 1 |
| Color_picture | BLOB | 0 | 1 |
| PK_UUID | UUID | 0 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### Tool_Maintenance

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| Tooling_Number | CLOB | 15 | 1 |
| MDate | TIMESTAMP | 19 | 1 |
| Revolutions | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 1 |

### Tooling

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| Number | CLOB | 15 | 1 |
| Flexo_HotS | CLOB | 30 | 1 |
| DieSize | REAL | 7 | 1 |
| SizeAcross | REAL | 7 | 1 |
| SizeAround | REAL | 7 | 1 |
| ColSpace | REAL | 7 | 1 |
| RowSpace | REAL | 7 | 1 |
| NoAcross | INT16 | 6 | 1 |
| NoAround | INT16 | 6 | 1 |
| LabelRepeat | REAL | 7 | 1 |
| GearTeeth | INT16 | 6 | 1 |
| Pitch | CLOB | 8 | 1 |
| Shape | CLOB | 40 | 1 |
| AutoApplied | BOOLEAN | 5 | 1 |
| DieCut | INT16 | 6 | 1 |
| LinerCaliper | CLOB | 15 | 1 |
| FaceStock | CLOB | 80 | 1 |
| Steel | CLOB | 10 | 1 |
| CornerRadius | REAL | 7 | 1 |
| SupplierID | CLOB | 10 | 1 |
| DateOrdered | TIMESTAMP | 19 | 1 |
| ToolIn | BOOLEAN | 5 | 1 |
| Price | REAL | 7 | 1 |
| ExclusiveUse | BOOLEAN | 5 | 1 |
| Revolutions | INT32 | 11 | 1 |
| Notes | CLOB | 0 | 1 |
| ChromePlate | BOOLEAN | 5 | 1 |
| Quantity | INT16 | 6 | 1 |
| Maint_subtable | INT32 | 11 | 1 |
| Owner | CLOB | 35 | 1 |
| Is_Used_by_eStore | BOOLEAN | 5 | 1 |
| Location | CLOB | 20 | 1 |
| Drawing | BLOB | 0 | 1 |
| Source_Appl | CLOB | 40 | 1 |
| File_Name | CLOB | 40 | 1 |
| DrawRptNotes | CLOB | 0 | 1 |
| PictDisplayFormat | CLOB | 30 | 1 |
| PictPrintFormat | CLOB | 30 | 1 |
| InternetQuery | BOOLEAN | 5 | 1 |
| SerialNumber | CLOB | 25 | 1 |
| Inactive | BOOLEAN | 5 | 1 |
| GearTeethRemainder | REAL | 7 | 1 |
| EnteredBy | CLOB | 50 | 1 |
| ModifiedBy | CLOB | 50 | 1 |
| EnteredDate | TIMESTAMP | 19 | 1 |
| ModifiedDate | TIMESTAMP | 19 | 1 |
| EnteredTime | INTERVAL | 10 | 1 |
| ModifiedTime | INTERVAL | 10 | 1 |
| Drawing_Size | REAL | 7 | 1 |
| Pitch_Local | CLOB | 0 | 1 |
| DieCut_Local | CLOB | 0 | 1 |
| PK_UUID | UUID | 0 | 1 |
| Flexo_HotS_Local | CLOB | 30 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |
| Tag | CLOB | 3 | 1 |
| cylinderColl | None | 0 | 1 |

### TraxxLink_PackingSlip_Log

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| PackingSlip_ID | CLOB | 10 | 1 |
| Ticket_ID | CLOB | 10 | 1 |
| Customer_ID | CLOB | 10 | 1 |
| Customer_Name | CLOB | 80 | 1 |
| Created_TimeStamp | INT32 | 11 | 1 |
| PackSlip_XML_Date_Created | TIMESTAMP | 19 | 1 |
| PackSlip_XML_Time_Created | INTERVAL | 10 | 1 |
| PackSlip_XML_Doc_Name | CLOB | 80 | 1 |
| PackSlip_XML_Content | BLOB | 0 | 1 |
| Invoice_ID | CLOB | 10 | 1 |
| Invoice_XML_Date_Created | TIMESTAMP | 19 | 1 |
| Invoice_XML_Time_Created | INTERVAL | 10 | 1 |
| Invoice_XML_Doc_Name | CLOB | 80 | 1 |
| Invoice_XML_Content | BLOB | 0 | 1 |
| Error_Message | CLOB | 0 | 1 |
| Is_Processed | BOOLEAN | 5 | 1 |
| Make_PackSlip_XML | BOOLEAN | 5 | 1 |
| Make_New_Invoice | BOOLEAN | 5 | 1 |
| Make_Invoice_XML | BOOLEAN | 5 | 1 |
| PK_UUID | UUID | 0 | 1 |

### UEFs

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| FormName | CLOB | 0 | 1 |
| InternalFormName | CLOB | 0 | 1 |
| TimeModified | INTERVAL | 10 | 1 |
| DateModified | TIMESTAMP | 19 | 1 |
| UserModified | CLOB | 80 | 1 |
| UEF_Exist | BOOLEAN | 5 | 1 |
| Table_Num | INT32 | 11 | 1 |
| Notes | CLOB | 0 | 1 |
| Use_ModifiedForm | BOOLEAN | 5 | 1 |
| Groups | CLOB | 40 | 1 |
| Hide | BOOLEAN | 5 | 1 |
| PK_UUID | UUID | 0 | 1 |

### UK_VAT

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| PK_UUID | UUID | 0 | 0 |
| Token | None | 0 | 1 |
| Data_User | None | 0 | 1 |
| Not_authorize | BOOLEAN | 5 | 1 |

### UniqueIDFile

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| FileNo | INT16 | 6 | 1 |
| IDNumber | CLOB | 20 | 1 |
| File_Name | CLOB | 31 | 1 |
| PK_UUID | UUID | 0 | 1 |

### UploadControl

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| Affiliate_ID | INT32 | 11 | 1 |
| FromDate | TIMESTAMP | 19 | 1 |
| ToDate | TIMESTAMP | 19 | 1 |
| ConnectionDate | TIMESTAMP | 19 | 1 |
| ConnectionTime | INTERVAL | 10 | 1 |
| NI_ForBalanceSheet | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |

### UploadData

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| UploadControl_ID | INT32 | 11 | 1 |
| Affiliate_ID | INT32 | 11 | 1 |
| AccountNumber | CLOB | 13 | 1 |
| AccountName | CLOB | 40 | 1 |
| FinancialStatementClass | CLOB | 40 | 1 |
| AcctTypeAbbr | CLOB | 2 | 1 |
| Balance | REAL | 7 | 1 |
| PK_UUID | UUID | 0 | 1 |

### UserFavorites

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 0 |
| EmployeeNumber | CLOB | 0 | 1 |
| AreaName | CLOB | 0 | 1 |
| Sort | INT32 | 11 | 1 |
| FavID | INT32 | 11 | 1 |
| PK_UUID | UUID | 0 | 0 |

### WIP_Parentage

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 60 | 1 |
| PK_UUID | UUID | 0 | 0 |
| Parent_IDNumber | CLOB | 255 | 1 |
| Child_IDNumber | CLOB | 255 | 1 |
| Parent_LengthUsed | INT32 | 11 | 1 |

### WorldshipData

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| PackingSlipNumber | CLOB | 10 | 1 |
| TrackingNum | CLOB | 40 | 1 |
| ShippingCost | CLOB | 40 | 1 |
| ReceivedFromUPSW_Date | TIMESTAMP | 19 | 1 |
| ReceivedFromUPSW_Time | INTERVAL | 10 | 1 |
| WrittenToPackingSlip_Date | TIMESTAMP | 19 | 1 |
| WrittenToPackingSlip_Time | INTERVAL | 10 | 1 |
| Cartons | CLOB | 40 | 1 |
| Weight | CLOB | 40 | 1 |
| Processed_Date | TIMESTAMP | 19 | 1 |
| Processed_Time | INTERVAL | 10 | 1 |
| PK_UUID | UUID | 0 | 1 |

### ZRec

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | INT32 | 11 | 1 |
| Alpha1 | CLOB | 40 | 1 |
| Alpha2 | CLOB | 40 | 1 |
| Alpha3 | CLOB | 40 | 1 |
| Alpha4 | CLOB | 40 | 1 |
| Alpha5 | CLOB | 40 | 1 |
| Alpha6 | CLOB | 40 | 1 |
| Alpha7 | CLOB | 40 | 1 |
| Alpha8 | CLOB | 40 | 1 |
| Alpha9 | CLOB | 40 | 1 |
| Alpha10 | CLOB | 20 | 1 |
| Alpha11 | CLOB | 20 | 1 |
| Alpha12 | CLOB | 40 | 1 |
| Alpha13 | CLOB | 40 | 1 |
| Alpha14 | CLOB | 40 | 1 |
| Alpha15 | CLOB | 40 | 1 |
| Alpha16 | CLOB | 40 | 1 |
| Alpha17 | CLOB | 40 | 1 |
| Alpha18 | CLOB | 40 | 1 |
| Alpha19 | CLOB | 40 | 1 |
| Alpha20 | CLOB | 40 | 1 |
| Alpha21 | CLOB | 20 | 1 |
| Pushed | BOOLEAN | 5 | 1 |
| Alpha22 | CLOB | 20 | 1 |
| Alpha23 | CLOB | 20 | 1 |
| Alpha24 | CLOB | 20 | 1 |
| Alpha25 | CLOB | 20 | 1 |
| Alpha26 | CLOB | 20 | 1 |
| Long1 | INT32 | 11 | 1 |
| Long2 | INT32 | 11 | 1 |
| Txt1 | CLOB | 0 | 1 |
| A_L15 | CLOB | 15 | 1 |
| A_L80 | CLOB | 80 | 1 |
| i1 | INT16 | 6 | 1 |
| Bool1 | BOOLEAN | 5 | 1 |
| SDate | TIMESTAMP | 19 | 1 |
| EDate | TIMESTAMP | 19 | 1 |
| STime | INTERVAL | 10 | 1 |
| ETime | INTERVAL | 10 | 1 |
| R1 | REAL | 7 | 1 |
| Bool2 | BOOLEAN | 5 | 1 |
| Bool3 | BOOLEAN | 5 | 1 |
| Bool4 | BOOLEAN | 5 | 1 |
| Date1 | TIMESTAMP | 19 | 1 |
| Date2 | TIMESTAMP | 19 | 1 |
| Elapsed | INTERVAL | 10 | 1 |
| Bool5 | BOOLEAN | 5 | 1 |
| Bool6 | BOOLEAN | 5 | 1 |
| Long3 | INT32 | 11 | 1 |
| Long4 | INT32 | 11 | 1 |
| Long5 | INT32 | 11 | 1 |
| Long6 | INT32 | 11 | 1 |
| Long7 | INT32 | 11 | 1 |
| Long8 | INT32 | 11 | 1 |
| Long9 | INT32 | 11 | 1 |
| Long10 | INT32 | 11 | 1 |
| Long11 | INT32 | 11 | 1 |
| Long12 | INT32 | 11 | 1 |
| R2 | REAL | 7 | 1 |
| R3 | REAL | 7 | 1 |
| R4 | REAL | 7 | 1 |
| R5 | REAL | 7 | 1 |
| R6 | REAL | 7 | 1 |
| R7 | REAL | 7 | 1 |
| R8 | REAL | 7 | 1 |
| R9 | REAL | 7 | 1 |
| R10 | REAL | 7 | 1 |
| R11 | REAL | 7 | 1 |
| R12 | REAL | 7 | 1 |
| R13 | REAL | 7 | 1 |
| Bool7 | BOOLEAN | 5 | 1 |
| R14 | REAL | 7 | 1 |
| R15 | REAL | 7 | 1 |
| R16 | REAL | 7 | 1 |
| R17 | REAL | 7 | 1 |
| R18 | REAL | 7 | 1 |
| R19 | REAL | 7 | 1 |
| R20 | REAL | 7 | 1 |
| R21 | REAL | 7 | 1 |
| R22 | REAL | 7 | 1 |
| R23 | REAL | 7 | 1 |
| R24 | REAL | 7 | 1 |
| R25 | REAL | 7 | 1 |
| R26 | REAL | 7 | 1 |
| R27 | REAL | 7 | 1 |
| R28 | REAL | 7 | 1 |
| R29 | REAL | 7 | 1 |
| R30 | REAL | 7 | 1 |
| R31 | REAL | 7 | 1 |
| R32 | REAL | 7 | 1 |
| R33 | REAL | 7 | 1 |
| R34 | REAL | 7 | 1 |
| R35 | REAL | 7 | 1 |
| R36 | REAL | 7 | 1 |
| R37 | REAL | 7 | 1 |
| R38 | REAL | 7 | 1 |
| R39 | REAL | 7 | 1 |
| R40 | REAL | 7 | 1 |
| R41 | REAL | 7 | 1 |
| R42 | REAL | 7 | 1 |
| R43 | REAL | 7 | 1 |
| Txt2 | CLOB | 0 | 1 |
| Txt3 | CLOB | 0 | 1 |
| Txt4 | CLOB | 0 | 1 |
| Txt5 | CLOB | 0 | 1 |
| Txt6 | CLOB | 0 | 1 |
| Txt7 | CLOB | 0 | 1 |
| Txt8 | CLOB | 0 | 1 |
| Txt9 | CLOB | 0 | 1 |
| PK_UUID | UUID | 0 | 1 |
| Long13 | INT32 | 11 | 1 |
| Long14 | INT32 | 11 | 1 |
| Long15 | INT32 | 11 | 1 |
| Long16 | INT32 | 11 | 1 |
| Long17 | INT32 | 11 | 1 |
| Long18 | INT32 | 11 | 1 |

### ZeroRec

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| ID | CLOB | 10 | 1 |
| i1 | INT16 | 6 | 1 |
| A20 | CLOB | 20 | 1 |
| A25 | CLOB | 25 | 1 |
| A30 | CLOB | 30 | 1 |
| A35 | CLOB | 35 | 1 |
| A80 | CLOB | 80 | 1 |
| A40_1 | CLOB | 40 | 1 |
| A40_2 | CLOB | 40 | 1 |
| Bool_1 | BOOLEAN | 5 | 1 |
| Note_1 | CLOB | 80 | 1 |
| Note_2 | CLOB | 80 | 1 |
| Txt_1 | CLOB | 0 | 1 |
| R1 | REAL | 7 | 1 |
| R2 | REAL | 7 | 1 |
| R3 | REAL | 7 | 1 |
| Pushed | BOOLEAN | 5 | 1 |
| R4 | REAL | 7 | 1 |
| R5 | REAL | 7 | 1 |
| Long1 | INT32 | 11 | 1 |
| Long2 | INT32 | 11 | 1 |
| Long3 | INT32 | 11 | 1 |
| Date1 | TIMESTAMP | 19 | 1 |
| Txt_2 | CLOB | 0 | 1 |
| A4ModID | CLOB | 20 | 1 |
| AP_Temp | CLOB | 20 | 1 |
| GL_Temp | CLOB | 20 | 1 |
| A20_2 | CLOB | 20 | 1 |
| A20_3 | CLOB | 20 | 1 |
| Date2 | TIMESTAMP | 19 | 1 |
| PK_UUID | UUID | 0 | 1 |

### deleteTrackingLog

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| pID | UUID | 0 | 0 |
| deleteTimeDateStamp | CLOB | 30 | 1 |
| TableNo | INT32 | 11 | 1 |
| TableName | CLOB | 40 | 1 |
| recordUUID | CLOB | 35 | 1 |

### glPrefixConst

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| PK_UUID | UUID | 0 | 0 |
| ID | CLOB | 10 | 1 |
| glLocationInfo | None | 0 | 1 |

### masterPS

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| pID | UUID | 0 | 0 |
| Number | CLOB | 10 | 1 |
| status | CLOB | 0 | 1 |
| creationDate | TIMESTAMP | 19 | 1 |
| shipDate | TIMESTAMP | 19 | 1 |
| location | CLOB | 0 | 1 |
| palletID | CLOB | 10 | 1 |

### multiLocation

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| PK_UUID | UUID | 0 | 0 |
| emp_MultiLocation | None | 0 | 1 |
| ID | CLOB | 0 | 1 |

### multiLocation_Main

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| PK_UUID | UUID | 0 | 0 |
| ID | CLOB | 0 | 1 |
| locationTag | CLOB | 255 | 1 |
| locationName | CLOB | 0 | 1 |
| Address1 | CLOB | 255 | 1 |
| Address2 | CLOB | 255 | 1 |
| City | CLOB | 255 | 1 |
| State_Province | CLOB | 255 | 1 |
| postCode | CLOB | 255 | 1 |
| Country | CLOB | 255 | 1 |
| Phone | CLOB | 255 | 1 |
| firstLocation | BOOLEAN | 5 | 1 |
| taxID | CLOB | 40 | 1 |
| mfgLogo | BLOB | 0 | 1 |
| accessStagingPS | BOOLEAN | 5 | 1 |
| newTimeDateStamp | CLOB | 30 | 1 |
| updateTimeDateStamp | CLOB | 30 | 1 |

### remoteDataCapture

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| PK_UUID | UUID | 0 | 0 |
| rdcClient | BOOLEAN | 5 | 1 |
| serverIP | CLOB | 45 | 1 |
| serverPort | CLOB | 5 | 1 |
| sensorSerialNumber | CLOB | 40 | 1 |
| workstationName | CLOB | 80 | 1 |
| equipmentNumber | CLOB | 10 | 1 |
| encoderSettings | None | 0 | 1 |
| useTLS | BOOLEAN | 5 | 1 |
| Tag | CLOB | 3 | 1 |
| AssocNum | CLOB | 10 | 1 |

### transitRequest

| column_name | type_name | column_size | nullable |
|---|---|---|---|
| PK_UUID | UUID | 0 | 0 |
| ID | CLOB | 0 | 1 |
| requestAssociateModule | CLOB | 0 | 1 |
| cylinderQuantity | INT16 | 6 | 1 |
| toolID | CLOB | 15 | 1 |
| Status | CLOB | 20 | 1 |
| requestedBy | CLOB | 255 | 1 |
| dateRequested | TIMESTAMP | 19 | 1 |
| dateRequired | TIMESTAMP | 19 | 1 |
| Status_org | CLOB | 20 | 1 |
| moveFrom | CLOB | 5 | 1 |
| moveTo | CLOB | 5 | 1 |
| Notes | CLOB | 0 | 1 |
| dateCreated | TIMESTAMP | 19 | 1 |
| type | CLOB | 25 | 1 |
