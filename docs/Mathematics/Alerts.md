# 告警(Alerts)

## style: callout

> [!NOTE]
> This is a simple Note type usage, all properties are default values.

---

> [!TIP]
> This is a simple TIP type usage, all properties are default values.

---

> [!WARNING]
> This is a simple WARNING type usage, all properties are default values.

---

> [!DANGER]
> This is a simple DANGER type usage, all properties are default values.

---

> [!COMMENT]
> An alert of type 'comment' using style 'callout' with default settings.

## style: flat

> [!NOTE|style:flat]
> This is a Note type usage, style: flat.

---

> [!TIP|style:flat]
> This is a TIP type usage, style: flat.

---

> [!WARNING|style:flat]
> This is a WARNING type usage, style: flat.

---

> [!DANGER|style:flat]
> This is a DANGER type usage, style: flat.

---

> [!COMMENT|style:flat]
> An alert of type 'comment' using style 'flat' with custom settings.

---

```
**[terminal]
**[prompt foo@joe]**[path ~]**[delimiter  $ ]**[command ./myscript]
Normal output line. Nothing special here...
But...
You can add some colors. What about a warning message?
**[warning [WARNING] The color depends on the theme. Could look normal too]
What about an error message?
**[error [ERROR] This is not the error you are looking for]
```

