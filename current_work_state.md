# ForgeNext Current Work State
## 現在作業状態

**Status:** CEO_ACTION_REQUIRED
**Owner:** CEO / CAO
**Updated:** 2026-07-19

---

## Current Work Item

ForgeNext Rule Engine Implementation

---

## Roadmap Position

Phase 3：Implementation

---

## Purpose

ForgeNextに既に存在するFoundation・Company Standard・Employee Standard・Blueprint・current_work_stateを、
AI社員の判断や注意力だけに依存せず、出力前に照合できる運営機構として実装する。

目的は、Arkを含むAI社員が意識せず会社基準を外れた場合でも、
不一致を検出し、出力または次工程への移行を停止できる状態を作ることである。

---

## Current State

`CEO_ACTION_REQUIRED`

---

## Approved Design Direction

Rule Engineは、新しい会社ルールを作る仕組みではない。

既存の会社基準を、出力前に機械的に照合する実行機構として実装する。

照合結果は最低限、次のいずれかとする。

- `PASS`
- `FAIL`
- `REVIEW_REQUIRED`

`FAIL` または `REVIEW_REQUIRED` の場合、
対象となる回答・提案・設計・実装・完了報告をそのまま提出してはならない。

Rule Engineは最終意思決定を行わない。
重要な不一致または判断不能事項はCEOへ可視化し、
最終意思決定権はCEOが保持する。

---

## Implementation Scope

### Stage 1：Standard Integration

1. `blueprint/01_Company/company_standard.md`
2. `blueprint/01_Company/employee_standard.md`
3. `blueprint/organization_audit.md`

既存文書へ、Rule Engineの実行順序・停止条件・監査責務を統合する。

### Stage 2：Executable Implementation

既存のPython構成を確認したうえで、
Rule Engineを実行可能な処理として実装する。

最低限、次を実現する。

1. 照合対象の読み込み
2. 必須確認項目の実行
3. PASS / FAIL / REVIEW_REQUIREDの判定
4. 不一致理由の記録
5. FAIL時の出力停止
6. 監査Evidenceの保存

### Stage 3：Operational Verification

次の3種類を検証する。

1. 正常系：適合する出力が通過する
2. 異常系：基準違反を検出して停止する
3. 回復系：修正後に再照合し、正常状態へ戻れる

---

## Rule Engine Minimum Checks

1. Purposeとの整合
2. Missionとの整合
3. Visionとの整合
4. Principlesとの整合
5. Company Constitutionとの整合
6. Company Standardとの整合
7. Employee Standardとの整合
8. Blueprint上の責務との整合
9. current_work_stateとの整合
10. CEO承認済み方針との整合
11. 既存運用・既存改善を先に検討したか
12. Evidence Verificationが必要か
13. 完了宣言と実体が一致しているか

---

## CEO Action Required

このファイルを指定内容へ置き換え、保存する。

---

## CAO Action After CEO Work

1. ファイルの存在確認
2. 全文確認
3. 承認内容との一致確認
4. Status確認
5. 次の実装対象を提示

---

## Evidence Required

次のいずれかを提出する。

- 保存後の `current_work_state.md` 全文
- 更新後に作成したBaseline Snapshot

---

## Completion Conditions

次のすべてを満たすまで、本作業を完了としてはならない。

1. current_work_stateが今回の作業へ更新されている
2. Company StandardへRule Engine運営原則が統合されている
3. Employee Standardへ出力前照合が統合されている
4. Organization Auditへ実行結果の独立確認責務が統合されている
5. Rule Engineが実行可能な形で実装されている
6. FAIL時に対象出力を停止できる
7. 判定理由とEvidenceが記録される
8. 正常系テストがPASSする
9. 異常系テストで違反を検出できる
10. 回復系テストで正常状態へ戻れる
11. Arkが試験内容を事前に知る出来レースだけに依存しない検証方法が実施される
12. Evidence Verificationが完了している
13. CEOが最終結果を確認している

---

## Transition Rule

現在のStatusが `CLOSED` になるまで、
Rule Engineと無関係な新規作業へ移行してはならない。

A（Advance）または続行指示は、
現在作業の次工程へ進む指示として解釈する。

---

## Status Definitions

- `IN_PROGRESS`：CAOまたはAI社員が作業中
- `CEO_ACTION_REQUIRED`：CEOの具体的作業待ち
- `EVIDENCE_PENDING`：実装済み・Evidence確認待ち
- `TESTING`：実証実験中
- `REVIEW_REQUIRED`：不一致またはCEO判断が必要
- `READY_TO_CLOSE`：全条件を満たしCEOの完了承認待ち
- `CLOSED`：正式完了