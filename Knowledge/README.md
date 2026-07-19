# Knowledge（知識資産）

**Status:** Design Active / Automation Not Yet Implemented

Knowledgeは、ForgeNextが業務を通じて得た経験を、再利用可能な会社資産へ変換し、検証・蓄積・反映・再利用するための循環機構である。

Knowledgeは、情報・出来事・作業ログを保存するだけの場所ではない。

会社全体が継続的に学習し、判断品質と実行品質を高め、Purposeをより実現できる会社へ成長するための中核システムである。

KnowledgeはBlueprintの配下ではない。

- Blueprintは、実証された会社の設計を安定して保持する。
- Knowledgeは、業務経験から会社を継続的に改善する。

両者は異なる責務を持ち、Knowledgeから必要な改善だけをBlueprintへ反映する。

---

# Responsibility（責務）

Knowledgeは次の責務を持つ。

## 1. Capture（候補収集）

各AI社員は、業務を通じて発生した次の情報から、再利用可能性のある内容をKnowledge候補として提出する。

- 成功から得た教訓
- 失敗から得た教訓
- 判断とその理由
- 実証された改善
- CEOとの新しい合意・約束
- AI社員の重要な気付き
- 再利用可能な設計原則
- 再利用可能な運用方法

出来事や会話そのものを正式Knowledgeとして登録しない。

---

## 2. Analyze（分析）

Knowledge候補を、将来の業務で再利用できる知識へ変換する。

分析では次を明確にする。

- 何が起きたか
- なぜ起きたか
- 何を学んだか
- どの業務で再利用できるか
- 既存のKnowledge・Blueprint・Standardと重複していないか

---

## 3. Verify（検証）

Knowledge候補は、必要に応じて次の確認を経て検証する。

- 実装
- 運用
- Evidence Verification
- CEOレビュー
- 責務監査

推測・未検証の内容は正式Knowledgeとしない。

---

## 4. Evaluate（会社基準による評価）

Knowledge候補は、次のFoundationを共通評価基準として判断する。

1. Purposeに沿っているか
2. Missionの実現に役立つか
3. Visionへ近づくか
4. Principlesに反していないか
5. 会社全体で再利用できるか

良いアイデアであることだけを理由に正式Knowledgeへ登録しない。

---

## 5. Preserve（資産化）

検証・評価を通過したKnowledgeだけを、正式な会社資産として保存する。

Knowledgeは個人やAIの記憶ではない。

人・AI・自動化処理が将来参照し、同じ判断品質と実行品質を再現できる状態で保存する。

---

## 6. Reflect（会社資産への反映）

正式Knowledgeは、必要性を確認したうえで、適切な会社資産へ反映する。

反映先の例：

- Blueprint
- Company Standard
- Employee Standard
- AI Standard
- Workflow
- テンプレート
- 実装コード

正式KnowledgeをすべてBlueprintへ反映してはならない。

会社全体への影響と責務を確認し、必要な内容だけを適切な場所へ反映する。

反映時は次の順序を守る。

1. 既存の運用で対応できないか確認する
2. 既存の文書・仕組みを改善できないか確認する
3. それでも不足する場合のみ新しい仕組みを追加する

---

## 7. Reuse（再利用）

AI社員は業務開始時に、担当業務に関係する正式Knowledgeを参照する。

Knowledgeは保存して終わらない。

次回の判断・設計・実装・運用へ利用されて初めて、会社資産として機能したと判断する。

---

## 8. Improve（循環）

Knowledgeを利用した業務から、新しい成功・失敗・判断・改善が生まれる。

それらを再びKnowledge候補として提出し、次の循環へ戻す。

Knowledgeのゴールは知識を増やすことではない。

会社が継続的に学習し、Purposeを以前より実現できる状態を作り続けることである。

Knowledge自身の仕組みも、運用結果に基づいて継続的に改善する。

---

## 9. Reject（登録しない判断）

次の内容は、正式Knowledgeとして登録しない。

- 一時的なメモ
- 単なる作業ログ
- 推測
- 実証されていない提案
- 個別案件にしか利用できない内容
- 既存Knowledgeとの重複
- Foundationと矛盾する内容
- 会社全体の判断品質・実行品質を高めない内容

登録しない場合は、必要に応じて却下理由を残す。

Knowledgeを増やすこと自体を目的としてはならない。

---

# Roles（役割分担）

## 専門AI社員

Research AI、Planning AI、Content AI、Image AI、Video AI、SNS AI、Analytics AIなどの専門AI社員は、専門業務に集中する。

業務中に得た気付きからKnowledge候補を提出するが、正式Knowledgeへの登録判断やBlueprint更新を単独で行わない。

## Knowledge AI

Knowledge AIは、Knowledge候補を受け取った時に起動するイベント駆動型AI社員とする。

主な責務：

- 候補の分析
- 重複確認
- 再利用可能性評価
- Foundationとの整合確認
- Evidence Verificationの確認
- 正式Knowledgeへの昇格判断
- Reject判断
- 反映先の提案
- Blueprint・Standard等の更新案作成
- Knowledge自身の改善

重要な反映・変更はCEOレビューを必要とする。

## CEO

CEOは、重要なKnowledgeの正式承認および会社資産への重要変更を最終判断する。

## CAO

CAOは、Knowledgeの設計と会社全体との整合性を監査し、責務の重複・欠落・複雑化を防止する。

---

# Knowledge Lifecycle（循環）

```text
Foundation確認
        ↓
業務開始
        ↓
業務実施
        ↓
気付き・成功・失敗・判断・改善・合意
        ↓
Knowledge候補提出
        ↓
Knowledge AI起動
        ↓
分析・重複確認・Foundation評価
        ↓
検証
        ↓
正式Knowledge または Reject
        ↓
必要な会社資産へ反映
        ↓
全AI社員が次回業務で参照
        ↓
新しい業務・新しい改善
        ↓
Knowledge候補へ戻る