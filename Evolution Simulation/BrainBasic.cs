using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BrainBasic : Brain
{
    public float moveMultiplier1 = 1;
    public float moveMultiplier2 = 1;
    public float turnMultiplier1 = 1;

    public float energyThreshold = 100;

    public override void Think(Dictionary<string, float> senses)
    {
        base.Think(senses);

        // Calculate swimDirection
        swimDirection = transform.up * moveMultiplier1;
        if (senses.ContainsKey("energy") && senses["energy"] > energyThreshold)
        {
            swimDirection += swimDirection*moveMultiplier2;
        }

        // Calculate turnForce
        turnForce = turnMultiplier1;

        energyUse = 1;
    }

    public override void InheritFromParent(Brain parentBrain)
    {
        base.InheritFromParent(parentBrain);
        
        if (parentBrain.GetType() == typeof(BrainBasic))
        {
            BrainBasic basicBrain = (BrainBasic)parentBrain;
            moveMultiplier1 = mutateMultiplier(basicBrain.moveMultiplier1);
            moveMultiplier2 = mutateMultiplier(basicBrain.moveMultiplier2);
            turnMultiplier1 = mutateMultiplier(basicBrain.turnMultiplier1);
        }
    }

    private float mutateMultiplier(float originalValue)
    {
        return originalValue + Random.Range(-.1f, .1f);
    }
}
